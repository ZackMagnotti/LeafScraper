import concurrent.futures as futures
import sys

import scraper
import util
from strain import StrainAncestorNode

'''
Best trees:
leafly.com/strains/purple-roze
leafly.com/strains/ice-cream-cake
leafly.com/strains/high-noon-irish-cream
leafly.com/strains/bonkers
leafly.com/strains/superstar
leafly.com/strains/future-1
leafly.com/strains/drizella
'''

options = '''

    More options:

    (help)
    (info)
    (quit)


    >>'''

greeting = '''

    Welcome to Strain Anscestry!

    Enter the name or Leafly.com url 
    of any cannabis strain to generate 
    that strain's ancestry tree
'''

help_message = '''

    <HELP>

    Type the name of a cannabis strain
    or copy paste the url of that strain's 
    Leafly.com page into the terminal to 
    see that strain's lineage
'''

info = '''

    <INFO>

    Some of the best trees:

    leafly.com/strains/purple-roze
    leafly.com/strains/ice-cream-cake
    leafly.com/strains/high-noon-irish-cream
    leafly.com/strains/bonkers
    leafly.com/strains/superstar
    leafly.com/strains/future-1
    leafly.com/strains/drizella
'''

def recursive_generate_tree(parent_links):

    def get_parent_node(parent_link):

        # printing a long space and then '\r' clears previous output
        long_space = ' '*50
        print(long_space, end='\r')
        print(f'fetching info from {parent_link}', end='\r')

        parent_url = util.sanitized_url(parent_link)
        parent_name, grandparent_links = scraper.get_name_and_parent_links(parent_url)
        '''
        HOTFIX

        A loop exists between 
        purple-kush and purple-afghani

        Cut the connection 
        purple-afghani -> purple-kush
        to destroy loop
        '''
        if '/strains/purple-afghani' == parent_link:
            if '/strains/purple-kush' in grandparent_links:
                grandparent_links.remove('/strains/purple-kush')

        parent_node = StrainAncestorNode(parent_name, parent_url)
        parent_node.strain_parents = recursive_generate_tree(grandparent_links)
        return parent_node

    # Threading allows script to make multiple http requests simultaneously to save time
    with futures.ThreadPoolExecutor() as e:
        threads = [e.submit(get_parent_node, parent_link) for parent_link in parent_links]
        parent_nodes = [thread.result() for thread in futures.as_completed(threads)]
            
    return parent_nodes


def get_input(message):
    return input(message + options).lower()

def space_to_dash(name):
    return name.replace(' ', '-')

def main():

    user_input = get_input(greeting)

    while True:
        if user_input == 'help':
            user_input = get_input(help_message)

        elif user_input == 'info':
            user_input = get_input(info)

        elif user_input == 'quit':
            print('\nBye!')
            sys.exit()
            break

        else:
            break

    root_url = util.sanitized_url(space_to_dash(user_input))
    root_name, parent_links = scraper.get_name_and_parent_links(root_url)

    message = f'''
    -------------------------------
    Root strain : {root_name}
    -------------------------------
    '''
    print(message)

    root = StrainAncestorNode(root_name, root_url)        
    root.strain_parents = recursive_generate_tree(parent_links)

    message = f'''\n
    -------------------------------
    {root_name} Ancestry Tree
    -------------------------------
    '''
    print(message)

    root.show_tree()

if __name__ == '__main__':
    main()
