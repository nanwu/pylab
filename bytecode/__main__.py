import marshal
import types

with open('a.pyc', 'rb') as f:
    magic = f.read(4)
    date = f.read(4)
    code = marshal.load(f)

def inspect_code_object(co, indent=''):
    print '%s%s(lineno:%d)' % (indent, co.co_name,
        co.co_firstlineno)
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            inspect_code_object(c, indent+'\t')

inspect_code_object(code)
