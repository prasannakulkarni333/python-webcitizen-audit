Not yet ready to be used. This is a work in progress.

The goal is to provide a set of utilities to extract information from a web page and perform a set of audits. 

TODO - The audits are based on the Web Content Accessibility Guidelines (WCAG) 2.1.

# python-webcitizen-audit
Python library. HTML is the input, a set of audits are performed. Results are returned in a score or detailed score.

# inspiration
Discovered this project after I started mine. It is a good source of inspiration.
https://github.com/sethblack/python-seo-analyzer/tree/master

## Release


python -m build
python -m twine upload --config-file "./.pypirc" --repository pypi dist/*

