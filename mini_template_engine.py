import re

template = """
  <h1>{{ customerName }}</h1>
    <ul>
    {% for user in users %}
      <li><a href="{{ user.url }}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>
"""

data_to_render = {
    'customerName': 'uber',
    'users': [
        {
            'url': 'myUrl',
            'username': 'myUsername'
        }
    ]
}

simple_replace_regex = r'(?P<simple_replace>{{\s*[\w.]+\s*}})'
loop_replace_regex = r'(?P<loop_replace>{%[\s\w]+%}\n)'
replace_regex = '|'.join([simple_replace_regex, loop_replace_regex])



regex_obj = re.compile(replace_regex)
replace_iter = regex_obj.finditer(template)

replace_scheduled = []
while True:
    try:
        match_obj = next(replace_iter)
    except StopIteration:
        break

    replace_type = match_obj.lastgroup
    
    if replace_type == 'simple_replace':
        replace_start_idx, replace_end_idx = match_obj.start(), match_obj.end()
        match_obj = re.search(r'\w+', match_obj.group(0))
        data = data_to_render[match_obj.group(0)]
	new_template = template[:replace_start_idx] + data + template[replace_end_idx:]
        replace_scheduled.append([(replace_start_idx, replace_end_idx),data])
    elif replace_type == 'loop_replace':
        loop_start_match_obj = match_obj
        loop_entry_match_objs = []
        while True:
            match_obj = next(replace_iter)
            if match_obj.lastgroup == 'simple_replace':
                loop_entry_match_objs.append(match_obj)
            else:
                break
        loop_end_match_obj = match_obj
        entry_in_loop = template[loop_start_match_obj.end():loop_end_match_obj.start()]
        
        words = re.findall(r'\w+', loop_start_match_obj.group(0))
        list_name = words[-1]
        
        last_idx = loop_start_match_obj.end()
        chunk_indices = []
        vars_to_replace = []
        for match_obj in loop_entry_match_objs:
            chunk_indices.append((last_idx, match_obj.start()))
            last_idx = match_obj.end()
            var_to_replace = re.search(r'[\w.]+', match_obj.group(0)).group(0)
            vars_to_replace.append(var_to_replace.split('.')[1])
        chunk_indices.append((last_idx, loop_end_match_obj.start()))
        chunks = [template[start_idx:end_idx] for start_idx, end_idx in chunk_indices]
        rows = []
        for entry in data_to_render[list_name]:
            vars_val = []
            for var_to_replace in vars_to_replace:    
                vars_val.append(entry[var_to_replace])
            vars_val.append('')
            rows.append(''.join([chunk + var for chunk, var in zip(chunks, vars_val)]))
        replace_scheduled.append([(loop_start_match_obj.start(), loop_end_match_obj.end()), '\n'.join(rows)])

last_idx = 0
chunks = []
for (start_idx, end_idx), data in replace_scheduled:
    chunks.append(template[last_idx:start_idx])
    chunks.append(data)
    last_idx = end_idx
chunks.append(template[last_idx:])

print ''.join(chunks)
