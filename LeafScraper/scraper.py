import requests
from bs4 import BeautifulSoup


class PageNotFoundError(Exception):
    pass

def is404(soup):
    '''
    Function to check if a page is the 404 error page

    INPUT
    ---------
    soup (BeautifulSoup) : the page to chec, as a BeautifulSoup object


    OUTPUT
    ---------
    (bool) : True if page is 404, false otherwise

    '''
    if '404' in soup.head.title.text:
        return True
    return False


def get_html_from_site(url):
    '''
    Function takes url of a webpage and returns the HTML of that page as a string.

    Uses requests module

    INPUT
    ---------
    url (string) : url of the webpage


    OUTPUT
    ---------
    (string) : the HTML of that page as a string
    '''
    return requests.get(url).text


def get_soup(url):
    '''
    Function takes url of a webpage and returns the HTML of that page as a BeautifulSoup object.

    Uses getHTML and BeautifulSoup module

    INPUT
    ---------
    url (string) : url of the webpage


    OUTPUT
    ---------
    strain_page (BeautifulSoup) : the HTML of that page as a BeautifulSoup object
    '''
    html = get_html_from_site(url)
    soup = BeautifulSoup(html, 'lxml')

    if is404(soup):
        raise PageNotFoundError("404 Page Not Found")

    return soup


def get_parent_links_from_soup(soup):
    '''
    Scrapes Strain page to find parent strain links

    INPUT
    ---------
    soup (BeautifulSoup) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    (list) : list containing the parent hrefs as strings
    '''
    parent_divs = (
            soup.find(class_ = 'lineage__left-parent'),
            soup.find(class_ = 'lineage__right-parent'),
            soup.find(class_ = 'lineage__center-parent')
        )

    return [ parent.a.get('href') for parent in parent_divs if parent is not None ]


def get_child_links_from_soup(soup):
    '''
    Scrapes Strain page to find child strain links

    INPUT
    ---------
    soup (BeautifulSoup) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    (list) : list containing the child hrefs as strings
    '''
    child_divs = (
            soup.find(class_='lineage__left-child--two-parents'),
            soup.find(class_='lineage__left-child--two-parents'),
            soup.find(class_='lineage__center-child--two-parents'),
            soup.find(class_='lineage__left-child--single-parent'),
            soup.find(class_='lineage__right-child--single-parent'),
            soup.find(class_='lineage__center-child--single-parent'),
            soup.find(class_='lineage__left-child--no-parents'),
            soup.find(class_='lineage__right-child--no-parents'),
            soup.find(class_='lineage__center-child--no-parents')
        )

    return [ child.a.get('href') for child in child_divs if child is not None ]


def get_name_from_soup(soup):
    '''
    Scrapes strain page to find strain name

    INPUT
    ---------
    soup (BeautifulSoup) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    name (string) : name of strain
    '''
    return soup.find('h1', itemprop = 'name').text


def get_name(url):
    '''
    Calls get_soup() and get_name_from_soup() to get strain name from given url

    INPUT
    ---------
    url (string) : string representing the url of the strain page


    OUTPUT
    ---------
    name (string) : name of strain
    '''
    soup = get_soup(url)
    return get_name_from_soup(soup)


def get_parents_links(url):
    '''
    Calls get_soup() and get_parent_links_from_soup() to
    get strain parents' url extensions as a string

    INPUT
    ---------
    url (string) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    (list) : list containing the parent hrefs as strings
    '''
    soup = get_soup(url)
    return get_parent_links_from_soup(soup)


def get_child_links(url):
    '''
    Calls get_soup() and get_child_links_from_soup()
    to get strain parents' url extensions as a string

    INPUT
    ---------
    url (string) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    (list) : list containing the child hrefs as strings
    '''
    soup = get_soup(url)
    return get_child_links_from_soup(soup)


def get_name_and_parent_links(url):
    '''
    Calls get_soup(), get_name_from_soup(), and get_parent_links_from_soup()
    to get strain's parents' url extensions as a string

    Having a version of these functions combined like this is
    useful to avoid requesting the same webpage twice

    INPUT
    ---------
    url (string) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    name (string) : name of strain
    parent_links (list) : list containing the parent hrefs as strings
    '''
    soup = get_soup(url)
    name = get_name_from_soup(soup)
    parent_links = get_parent_links_from_soup(soup)
    return name, parent_links


def get_name_and_child_links(url):
    '''
    Calls get_soup(), get_name_from_soup(), and get_child_links_from_soup()
    to get strain's children's url extensions as a string

    Having a version of these functions combined like this is
    useful to avoid requesting the same webpage twice

    INPUT
    ---------
    url (string) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    name (string) : name of strain
    parents (list) : list containing the parent hrefs as strings
    '''
    soup = get_soup(url)
    name = get_name_from_soup(soup)
    child_links = get_child_links_from_soup(soup)
    return name, child_links


def main():
    url = 'https://www.leafly.com/strains/green-crack'

    name, children = get_name_and_child_links(url)

    print(name)

    for child in children:
        print(child)




if __name__ == '__main__':
    main()