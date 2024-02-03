# open file
import requests

html_text_to_check = requests.get('https://www.google.com').text


print(html_text_to_check)

"""


def traversecheck_html(html:str):
    import bs4
    x = bs4.BeautifulSoup(html, 'html.parser')
    # get meta viewport tag value
    message = []
    score = 0
    meta_viewport_value = x.find('meta', {'name': 'viewport'})
    print((meta_viewport_value))
    meta_viewport_value = meta_viewport_value.get('content')
    if str(meta_viewport_value) == 'width=device-width, initial-scale=1.0':
        score += 10
        message.append('Meta viewport tag is set correctly')
    # get all links
    # for link in x.find_all('a'):
        # print(link.get('href'))
    return score, message
traversecheck_html(html_text_to_check)
"""