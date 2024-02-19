This is a work in progress. Function are subject to change.

The goal is to provide a set of utilities to extract information from a web page and perform a set of audits. 

TODO - The audits are based on the Web Content Accessibility Guidelines (WCAG) 2.1.

# python-webcitizen-audit
Python library. HTML is the input, a set of audits are performed. Results are returned in a score or detailed score.

This is not a web crawler. You need to provide the HTML content as a string or mention URL, description etc manually while creating an object.

# inspiration
Discovered this project after I started mine. It is a good source of inspiration.
https://github.com/sethblack/python-seo-analyzer/tree/master

## Release


python -m build && python -m twine upload --config-file "./.pypirc" --repository pypi dist/*

