import requests
from bs4 import BeautifulSoup

class PageNotFoundError(Exception):
    pass

def is404(soup):
    '''
    Function to check if a page is the 404 error page

    INPUT
    ---------
    soup (BeautifulSoup) : the page to check, as a BeautifulSoup object


    OUTPUT
    ---------
    (bool) : True if page is 404, false otherwise
    '''
    if '404' in soup.head.title.text:
        return True
    return False

def lineage_not_found(soup):
    '''
    Function takes in Beautiful Soup object of
    strain page and determines if page has lineage data

    INPUT
    ---------
    soup (BeautifulSoup) : the page to check, as a BeautifulSoup object


    OUTPUT
    ---------
    (bool) : True if page has no lineage data, false otherwise
    '''
    headers = [h2.text.lower() for h2 in soup.find_all('h2')]
    if 'lineage' in headers:
        return False
    return True

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
    
    Raises error if page is the 404 page

    INPUT
    ---------
    url (string) : url of the webpage


    OUTPUT
    ---------
    (BeautifulSoup) : the HTML of that page as a BeautifulSoup object
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

    return [ parent.a.get('href') for parent in parent_divs if parent ]

def get_name_from_soup(soup):
    '''
    Scrapes strain page to find strain name

    INPUT
    ---------
    soup (BeautifulSoup) : BeautifulSoup object representing the strain page


    OUTPUT
    ---------
    (string) : name of strain
    '''
    return soup.find('h1', itemprop = 'name').text

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
    (string) : name of strain
    (list) : list containing the parent hrefs as strings
    '''
    soup = get_soup(url)
    return get_name_from_soup(soup), get_parent_links_from_soup(soup)