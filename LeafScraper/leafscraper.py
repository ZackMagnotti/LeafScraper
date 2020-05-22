import concurrent.futures as futures
import sys

import scraper
import util
from strain import StrainAncestorNode, StrainDescendantNode


def get_parent_node(parent_url, recursive_function):

    parent_name, grandparent_links = scraper.get_name_and_parent_links(parent_url)
    '''
    HOTFIX

    A loop exists between 
    purple-kush and purple-afghani

    Cut the connection 
    purple-afghani -> purple-kush
    to destroy loop
    '''
    if 'https://www.leafly.com//strains/purple-afghani' == parent_url:
        if '/strains/purple-kush' in grandparent_links:
            grandparent_links.remove('/strains/purple-kush')

    parent_node = StrainAncestorNode(parent_name, parent_url)
    parent_node.strain_parents = recursive_function(grandparent_links, get_parent_node)

    return parent_node

    

def get_child_node(child_url, recursive_function):

    child_name, grandchild_links = scraper.get_name_and_child_links(child_url)
    child_node = StrainDescendantNode(child_name, child_url)
    child_node.children = recursive_function(grandchild_links, get_child_node)

    return child_node


def recursive_generate_tree(links, function):

    def get_node(link, function):
        # printing a long space and then '\r' clears previous output
        print(' '*50, end='\r')
        print(f'fetching info from {link}', end='\r')
        url = util.sanitized_url(link)
        return function(url, recursive_generate_tree)

    # Threading allows script to make multiple http requests simultaneously to save time
    with futures.ThreadPoolExecutor() as e:
        threads = [e.submit(get_node, link, function) for link in links]
        nodes = [thread.result() for thread in futures.as_completed(threads)]
            
    return nodes


def main():
    url = 'https://www.leafly.com/strains/afghani'

    string = '''
    ------------------------
     Afgani Descendant Tree
    ------------------------
    '''

    print(string)

    node_type = 'descendant'

    if node_type.lower() == 'ancestor':
        name, parent_links = scraper.get_name_and_parent_links(url)
        root = StrainAncestorNode(name, url)
        root.strain_parents = recursive_generate_tree(parent_links, get_parent_node)

    elif node_type.lower() == 'descendant':
        name, child_links = scraper.get_name_and_child_links(url)
        root = StrainDescendantNode(name, url)
        root.children = recursive_generate_tree(child_links, get_child_node)

    else:
        print('invalid')
        sys.exit()

    print('\n')

    root.show_tree()
    
if __name__ == '__main__':
    main()