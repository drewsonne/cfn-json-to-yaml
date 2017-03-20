#! /usr/bin/env python
import json
import sys

# file = sys.argv[1]
file = '/Users/drews/Development/bookatable-infrastructure-as-code/CloudFormation/Templates/VPCScaffold.sections'

with open(file, 'r') as fp:
    structure = json.loads(fp.read())

def walk_tree(tree):

    return map(process_node, tree)

    # for key, struct in tree:
    #     process_node(struct, key)

def process_node(node_key):
    node, key = node_key
    if type(node) == dict:
        return walk_tree(node)
    elif type(node) in [list, tuple]:
        return map(process_node, node)
    else:
        # print("Type: {type}, Key: {key}".format(key=key, type=type(node)))
        print("Type: {type}".format(type=type(node)))
        return node if key is None else (key, node)

new_tree = walk_tree(structure.items())

print(new_tree)
