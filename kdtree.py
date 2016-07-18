import math
from collections import namedtuple
from operator import itemgetter
from pprint import pformat

class Node(namedtuple('Node', 'pos left right')):
    def __repr__(self):
        return pformat(tuple(self))

def build_kdtree(positions, depth):
    try:
        axis = depth % len(positions[0])
    except IndexError:
        return None

    positions.sort(key=itemgetter(axis))    
    mid_idx = len(positions) / 2
    return Node(positions[mid_idx], 
                build_kdtree(positions[:mid_idx], (axis + 1)%2),
                build_kdtree(positions[mid_idx+1:], (axis + 1)%2))


def dist_sqrd(n1, n2):
    dis = 0.0
    for i, val in enumerate(n1.pos):
        dis += (val - n2.pos[i]) ** 2
    return dis 

def search_nearest(node, target):
    nn, min_dist_sqrd = None, sys.maxint
    global nn, min_dist_sqrd

    def helper(node, target, depth=1):
        if not node:
            return
        
        global nn, min_dist_sqrd
        axis = depth % len(node.pos)
        if node.pos[axis] < target.pos[axis]:
            near_hp_child = node.right
            further_hp_child = node.left
        else:
            near_hp_child = node.left
            further_hp_child = node.right

        helper(near_hp_child, target, depth+1)
        if dist_sqrd(node, target) ** 2 < min_dist_sqrd:
            nn = node
            min_dis_sqrd = dist_sqrd(node, target)

        if further_hp_child and abs(nn.pos[axis] - target.pos[axis]) > abs(node.pos[axis] - target.pos[axis]):
            helper(further_hp_child, target, depth+1) 
        
    return nn
    
root_node = build_kdtree([(1, 2), (3, 4)], 0)
print root_node
