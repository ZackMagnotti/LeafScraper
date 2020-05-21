class URLError(ValueError):
    '''
    Error raised when input url is invalid
    '''
    pass

https, www, site, extension = 'https://', 'www.', 'leafly.com', '/strains'

url_template = [https, www, site, extension, '/']

template_string = ''.join(url_template)

def sanitized_url(input_url):
    '''
    Takes input and attempts to form it into a valid url, and
    before returning checks validity.

    Example:

    if input_url -> extension/page

    output -> https://www.example.com/extension/page
    '''
    url = input_url
    for i, elem in enumerate(reversed(url_template)):
        if elem not in url:
            url = ''.join(url_template[:len(url_template)-i]) + url
            break

    if url[:len(template_string)] != template_string:
        raise URLError("Invalid URL")

    if not url > template_string:
        raise URLError("Invalid URL")

    return url