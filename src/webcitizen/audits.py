# open file
import bs4
import newspaper

def responsive_check(html:str):
    """
    Check if the website is responsive
    Args:
    html (str): html content of the website
    Returns:
    int: score
    list: message
    """    
    x = bs4.BeautifulSoup(html, 'html.parser')
    # get meta viewport tag value
    message = []
    score = 0
    if str(x.find('meta', {'name': 'viewport'}).get('content')) == 'width=device-width, initial-scale=1.0':
        score += 10
        message.append('Meta viewport tag is set correctly')
    # check if there are media queries in the html 
    if '@media' in html:
        score += 10
        message.append('Media queries are present')
    if "max-width" in html:
        score += 10
        message.append('Max-width is present')
    
    return score, message

def searchengine_check(html:str):
    """
    Check if the website is search engine friendly
    Args:
    html (str): html content of the website
    Returns:
    int: score
    list: message
    """
    x = bs4.BeautifulSoup(html, 'html.parser')
    # get meta viewport tag value
    message = []
    score = 0
    # check if there are meta description tag
    if x.find('meta', {'name': 'description'}):
        score += 10
        message.append('Meta description tag is present')
    # check if page has H1 tag
    if x.find('h1'):
        score += 10
        message.append('H1 tag is present')
    
    return score, message
