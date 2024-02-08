from webpage import Webpage

import requests

url_ = "https://prasannakulkarni.com"
obj = Webpage(url=url_, html=requests.get(url_).text)

print(obj.json_html2())
