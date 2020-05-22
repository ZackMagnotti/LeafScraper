import concurrent.futures as futures

import scraper
import util
from strain import StrainAncestorNode, StrainDescendantNode


def get_parent_node(parent_url, recursive_function):

    try:
        parent_name, grandparent_links = scraper.get_name_and_parent_links(parent_url)
    
    except scraper.LineageNotFoundError:
        parent_name = scraper.get_name(parent_url)
        grandparent_links = []

    '''
    HOTFIX

    A loop exists between 
    purple-kush and purple-afghani

    Cut the connection 
    purple-afghani -> purple-kush
    to destroy loop
    '''
    if 'https://www.leafly.com/strains/purple-afghani' == parent_url:
        if '/strains/purple-kush' in grandparent_links:
            grandparent_links.remove('/strains/purple-kush')

    parent_node = StrainAncestorNode(parent_name, parent_url)
    if grandparent_links:
        parent_node.strain_parents = recursive_function(grandparent_links, get_parent_node)

    return parent_node


def get_child_node(child_url, recursive_function):

    try:
        child_name, grandchild_links = scraper.get_name_and_child_links(child_url)

    except scraper.LineageNotFoundError:
        child_name = scraper.get_name(child_url)
        grandchild_links = []

    child_node = StrainDescendantNode(child_name, child_url)
    if grandchild_links:
        child_node.children = recursive_function(grandchild_links, get_child_node)

    return child_node


def recursive_generate_tree(links, function):

    def get_node(link, function):
        # printing a long space and then '\r' clears previous output
        print(f'    fetching info from {link}' + ' '*20, end='\r')
        url = util.sanitized_url(link) 
        return function(url, recursive_generate_tree)

    # Threading allows script to make multiple http requests simultaneously to save time
    with futures.ThreadPoolExecutor() as e:
        threads = [e.submit(get_node, link, function) for link in links]
        nodes = [thread.result() for thread in futures.as_completed(threads)]
            
    return nodes


def generate_ancester_tree(root_url):
    try:
        name, parent_links = scraper.get_name_and_parent_links(root_url)

    except scraper.LineageNotFoundError:
        name = scraper.get_name(root_url)
        message = f'''
    -------------------------------
    No Lineage Data for {name}
    -------------------------------
        '''
        print(message)
        raise scraper.LineageNotFoundError

    message = f'''
    -------------------------------
    Root strain : {name}
    -------------------------------
    '''
    print(message)
    root = StrainAncestorNode(name, root_url)
    root.strain_parents = recursive_generate_tree(parent_links, function=get_parent_node)
    return root


def generate_descendant_tree(root_url):
    try:
        name, child_links = scraper.get_name_and_child_links(root_url)

    except scraper.LineageNotFoundError:
        name = scraper.get_name(root_url)
        message = f'''
    -------------------------------
    No Lineage Data for {name}
    -------------------------------
        '''
        print(message)
        raise scraper.LineageNotFoundError

    message = f'''
    -------------------------------
    Root strain : {name}
    -------------------------------
    '''
    print(message)
    root = StrainDescendantNode(name, root_url)
    root.children = recursive_generate_tree(child_links, function=get_child_node)
    return root


main_options = '''

    More options:

    (help)
    (info)
    (quit)


    >>'''

main_message = '''

    Enter the name or Leafly.com
    url of any cannabis strain
'''

help_message = '''

    <HELP>

    Type the name of a cannabis strain
    or copy paste the url of that strain's 
    Leafly.com page into the terminal to 
    see that strain's lineage
'''

info_message = '''

    <INFO>

    Some of the best trees:

    (ancestry)
    leafly.com/strains/purple-roze
    leafly.com/strains/ice-cream-cake
    leafly.com/strains/high-noon-irish-cream
    leafly.com/strains/bonkers
    leafly.com/strains/superstar
    leafly.com/strains/future-1
    leafly.com/strains/drizella
'''

tree_options = '''

    Tree Options:

    (ancestors)
    (descendants)
    (back)
    (quit)


    >>'''

invalid = '''
    INVALID'''

def get_input(message):
    return input(message).lower()


def space_to_dash(name):
    return name.replace(' ', '-')


def main():

    # MAIN MENU
    user_input = get_input(main_message + main_options)

    while True:
        if user_input == 'help':
            user_input = get_input(help_message+main_options)

        elif user_input == 'info':
            user_input = get_input(info_message+main_options)

        elif user_input == 'quit':
            return False

        else:
            break
    
    try:
        name = user_input
        root_url = util.sanitized_url(space_to_dash(user_input))
    
    except util.URLError:
        print("\n    Sorry! Looks like we couldn't turn your input into a valid Leafly.com/strains url")
        user_input = input('\n    Try again? (y/n): ')
        if user_input == 'yes' or user_input == 'y':
            return True
        return False

    # Tree Menu
    try:
        while True:

            user_input = get_input(tree_options)

            if user_input == 'ancestors':
                root = generate_ancester_tree(root_url)
                break

            elif user_input == 'descendants':
                root = generate_descendant_tree(root_url)
                break

            elif user_input == 'back':
                return True

            elif user_input == 'quit':
                return False

            else:
                print(invalid)

    except scraper.LineageNotFoundError:
        pass
        
    except scraper.PageNotFoundError:
        print(f'''\n    Sorry! The page for "{name}" doesn't exist''')
        user_input = input('\n    Try again? (y/n): ')
        if user_input == 'yes' or user_input == 'y':
            return True
        return False

    else:
        # printing a long space and then '\r' clears previous output
        print('\r    Done!' + ' '*60)
        message = f'''
    -------------------------------
    {root.name} Ancestry Tree
    -------------------------------
        '''
        print(message)

        root.show_tree()

    user_input = get_input('\nGo again? (y/n) : ')
    if user_input == 'yes' or user_input == 'y':
        return True
    return False

    
if __name__ == '__main__':
    greeting = '''\n\n    Welcome to Leaf Scraper!'''
    print(greeting)
    while main():
        pass
    print('\n    Bye!')
    input()
