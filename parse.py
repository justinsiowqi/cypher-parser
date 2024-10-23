import re
import json
import subprocess


# Use Libcypher Parser to Parse the Cypher Statement
def run_cypher_lint(cyp_file_path):
    try:
        # Execute the cypher-lint command
        result = subprocess.run(
            ['cypher-lint', '-a', cyp_file_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running cypher-lint:", e.stderr)
        return None
    
    
# Extract a Parsed Tree from Libcypher Parser Output
parse_tree = []
pattern = re.compile(
    r'^@(\d+)\s+'         # @<id> followed by spaces
    r'(\d+\.\.\d+)\s+'    # <span> followed by spaces
    r'([> ]*)\s+'         # Hierarchy indicators (>, spaces) followed by spaces
    r'([\w\[\]{}: ]+)\s+' # node_type (allowing spaces) followed by spaces
    r'(.*)$'              # details (rest of the line)
)

def extract_parse_tree(output):
    for line in output.split("\n"): 
        line = line.strip()           
        match = pattern.match(line)
        if match:
            node_id, span, hierarchy, node_type, details = match.groups()
            # print(f"Node ID: {node_id}")  

            level = hierarchy.count('>') 

            node = {
                'id': int(node_id),
                'span': span,
                'level': level,
                'type': node_type.strip(),
                'details': details.strip(),
                'children': []
            }
            parse_tree.append(node)
        else:
            if line:  
                print(f"Error: Unmatched line: {line}")
    return parse_tree


# Build a Hierarchical Tree Based on the Parsed Tree
def build_hierarchy(parse_tree):
    tree = []
    stack = []

    for node in parse_tree:
        current_level = node['level']
        node_info = {
            'id': node['id'],
            'span': node['span'],
            'type': node['type'],
            'details': node['details'],
            'children': []
        }

        if current_level == 0:
            tree.append(node_info)
            stack = [node_info]
        else:
            while len(stack) > current_level:
                stack.pop()
            if stack:
                parent = stack[-1]
                parent['children'].append(node_info)
                stack.append(node_info)
            else:
                tree.append(node_info)
                stack = [node_info]

    return tree


def split_individual_trees(parse_tree):
    
    # Get the IDs of the Statements
    item_list = []
    for item in parse_tree:
        if item["type"] == "statement":
            item_list.append(item)

    # Extract the Start ID and End ID of Each Individual Tree
    current_id = []
    parse_trees_ids = []

    for item in item_list:
        if not current_id:
            current_id.append(item["id"])
        else:
            if item["id"] != current_id[0]:
                parse_trees_ids.append((current_id[0], item["id"]))
                current_id = [item["id"]]

    if current_id:
        parse_trees_ids.append((current_id[0], parse_tree[-1]["id"]))
        
    # Use the Start ID and End ID to Index and Split the Parsed Trees 
    parse_trees = []
    for start_id, end_id in parse_trees_ids:
        parse_trees.append(parse_tree[start_id:end_id])

    return parse_trees


if __name__ == "__main__":
    
    # Use Libcypher Parser to Parse Cypher Statements
    cyp_file = 'sample.cyp'
    output = run_cypher_lint(cyp_file)
    
    # Extract Parsed Trees and Hierarchical Trees from Libcypher Parser Output
    parse_tree = extract_parse_tree(output)
    hierarchical_tree = build_hierarchy(parse_tree)
    
    # Extract the Individual Parsed Trees
    parse_tree_list = split_individual_trees(parse_tree)
    for tree in parse_tree_list:
        print(tree)