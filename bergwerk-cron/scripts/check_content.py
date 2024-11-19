import requests

LANGUAGES =  ['Deutsch', 'English']

HOST = "http://bergwerk-api/wiki/menuinput/"

def get_node(menuinput, language):
    payload = {"menuinput": menuinput, "language": language, "uid": "cron"}
    response = requests.post(HOST, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def build_tree(menuinput, parent=None, visited=None, missing_nodes=None, nodes_without_text=None, language=None):
    if visited is None:
        visited = set()
    if missing_nodes is None:
        missing_nodes = {}
    if nodes_without_text is None:
        nodes_without_text = set()

    if menuinput in visited:
        return
    visited.add(menuinput)

    node = get_node(menuinput, language)
    if node is None:
        parent_display = parent if parent is not None else 'Root'
        if menuinput not in missing_nodes:
            missing_nodes[menuinput] = set()
        missing_nodes[menuinput].add(parent_display)
        print(f"Node '{menuinput}' is missing. Referenced by '{parent_display}'")
        return

    if not node.get('text'):
        nodes_without_text.add(menuinput)
        print(f"Node '{menuinput}' has no text.")

    menuitems = node.get('menuitems', [])
    for item in menuitems:
        link = item.get('link')
        if link:
            build_tree(link, menuinput, visited, missing_nodes, nodes_without_text, language=language)

    return visited, missing_nodes, nodes_without_text

if __name__ == '__main__':

    for l in LANGUAGES:
        print(f"\nChecking language: {l}")
        visited_nodes, missing_nodes, nodes_without_text = build_tree('Start', language=l)

        print(f"\nVisited nodes: {visited_nodes}")
        if missing_nodes:
            print("\nMissing nodes and their references:")
            for missing_node, parents in missing_nodes.items():
                parent_list = ', '.join(parents)
                print(f"Node '{missing_node}' is missing. Referenced by: {parent_list}")
        if nodes_without_text:
            print(f"\nNodes without text: {nodes_without_text}")
