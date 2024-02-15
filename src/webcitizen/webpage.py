from urllib.parse import urlparse
from newspaper import Article
import bs4
from w3lib.html import replace_escape_chars
from typing import Optional
import pyap
import re


class Webpage:

    def __init__(
        self,
        url: str,
        html: Optional[str] = None,
        **kwargs,
    ) -> None:
        html = html.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")
        self.html = html
        if self.html is not None:

            article = Article(url)
            self.soup = bs4.BeautifulSoup(self.html, "html.parser")
            article.set_html(self.html)
            article.parse()
            article.nlp()
            self.article = article
            self.text = self.extract_text()

        self.url = url
        self.title = "" if kwargs.get("title") is None else kwargs.get("title")
        self.meta_description = (
            ""
            if kwargs.get("meta_description") is None
            else kwargs.get("meta_description")
        )
        self.h1 = "" if kwargs.get("h1") is None else kwargs.get("h1")

    def parse_self_from_html(self):
        parsed = self.json_html()
        parsed = parsed[0]
        keys, values = list(parsed.keys()), list(parsed.values())
        for i in range(len(keys)):
            setattr(self, keys[i], values[i])

    def __str__(self):
        return f"url: {self.url}, text: {self.text[:100]}..."

    def filter_links(self):
        all_links = self.soup.find_all("a", href=True)
        all_links = [x.get("href") for x in all_links]
        netloc = urlparse(self.url).netloc
        data = [
            f"https://{netloc}{x}" if x.startswith("//") else x
            for x in list(set(all_links))
        ]

        return {
            "external": [
                x
                for x in data
                if (bool(re.match(r"https?://", x)) or bool(re.match(r"//", x)))
                and (netloc not in x)
            ],
            "internal": [
                x
                for x in data
                if (not bool(re.match(r"https?://", x)))
                and (not bool(re.match(r"#", x)))
            ],
            "internal_same_domain": [
                x
                for x in data
                if (not bool(re.match(r"https?://", x)))
                and (not bool(re.match(r"#", x)))
                and (netloc in x)
            ],
            "external-domains": [
                urlparse(x).scheme + "://" + urlparse(x).netloc + "/"
                for x in data
                if (bool(re.match(r"https?://", x)) or bool(re.match(r"//", x)))
                and (netloc not in x)
            ],
        }

    def unpack_url(self, *args, **kwargs):

        _ = urlparse(self.url)
        dict_ = {
            "domain": _.netloc,
            "root_path": _.path.split("/")[1] if len(_.path.split("/")) > 1 else None,
            "full_path": _.path,
            "scheme": _.scheme,
            "scheme_domain": _.scheme,
            "base_url": f"{_.scheme}://{_.netloc}",
        }
        if kwargs.get("return_only"):
            v = kwargs.get("return_only")
            return dict_[v]
        else:
            return dict_

    def extract_text(self) -> str:

        new = self.soup
        new = replace_escape_chars(new.text, replace_by=" ")
        return " ".join(new.split())

    def extract_article_text(self) -> str:
        return self.article.text

    def json_nltk_article(self) -> dict:

        article = self.article

        _ = {
            "keywords": article.keywords,
            "summary": article.summary,
            "text": article.text,
            "title": article.title,
            "authors": article.authors,
            "publish_date": str(article.publish_date),
            "top_image": article.top_image,
            "meta_keywords": article.meta_keywords,
            "meta_description": article.meta_description,
            "meta_lang": article.meta_lang,
            "meta_favicon": article.meta_favicon,
            "canonical_link": article.canonical_link,
            "tags": list(article.tags),
            "movies": article.movies,
            "imgs": list(article.imgs),
        }
        return _

    def json_html(self, find_img_sizes=False) -> dict:
        base_url = self.unpack_url(return_only="base_url")
        images = self.soup.find_all("img")
        if find_img_sizes:
            img_sizes = {}
            for _ in [x.get("src") for x in images]:
                x = base_url + _ if _.startswith("/") else _
                import requests

                r = requests.head(x)
                img_sizes.__setitem__(x, int(r.headers.get("content-length")) / 1000000)

        addresses = (
            pyap.parse(self.text, country="US")
            + pyap.parse(self.text, country="GB")
            + pyap.parse(self.text, country="CA")
        )
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.text)

        # get all h1, h2, h3, h4, h5, h6, p, img, a, meta, link, script, style, title, keywords, description
        soup = self.soup
        phones = re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", self.text)
        json_html = {
            "phone_numbers": phones if len(phones) > 0 else None,
            "addresses": str(addresses) if len(addresses) > 0 else None,
            "emails": (emails) if len(emails) > 0 else None,
            "h1": [replace_escape_chars(i.text.strip()) for i in soup.find_all("h1")],
            "h2": [replace_escape_chars(i.text.strip()) for i in soup.find_all("h2")],
            "h3": [replace_escape_chars(i.text.strip()) for i in soup.find_all("h3")],
            "h4": [replace_escape_chars(i.text.strip()) for i in soup.find_all("h4")],
            "h5": [replace_escape_chars(i.text.strip()) for i in soup.find_all("h5")],
            "h6": [replace_escape_chars(i.text.strip()) for i in soup.find_all("h6")],
            "title": replace_escape_chars(soup.title.text.strip()),
            "keywords": (
                replace_escape_chars(
                    soup.find("meta", {"name": "keywords"}).get("content")
                )
                if soup.find("meta", {"name": "keywords"})
                else None
            ),
            "meta_description": (
                replace_escape_chars(
                    soup.find("meta", {"name": "description"}).get("content")
                )
                if soup.find("meta", {"name": "description"})
                else None
            ),
            "robots": (
                replace_escape_chars(
                    soup.find("meta", {"name": "robots"}).get("content")
                )
                if soup.find("meta", {"name": "robots"})
                else None
            ),
            "text_size": len(replace_escape_chars(soup.text.strip())),
        }

        if find_img_sizes:
            _ = {
                "img_sizes": img_sizes,
                "img_larger_than_1mb": [
                    img for img, size in img_sizes.items() if size > 1
                ],
            }
            json_html = {**json_html, **_}

        return json_html

    def analyze_meta_description(self) -> str:
        """
        Analyze the meta description of the website
        Args:
        url (str): url of the website
        html (str): html content of the website
        Returns:
        str: meta description of the website
        """
        if self.meta_description is None:
            self.meta_description = ""
        if self.meta_description:
            if len(self.meta_description) == 0:
                return "empty"
            elif len(self.meta_description) > 0 or len(self.meta_description) <= 129:
                return "short"
            elif len(self.meta_description) >= 130 or len(self.meta_description) <= 160:
                return "correct length"
            else:
                return "long"

    def analyze_H1(self) -> str:
        """
        Analyze the H1 of the website
        Args:
        url (str): url of the website
        html (str): html content of the website
        Returns:
        str: H1 of the website
        """
        if self.h1 is None:
            self.h1 = ""
        if self.h1:
            if len(self.h1) == 0:
                return "empty"
            elif len(self.h1) > 0 or len(self.h1) < 20:
                return "short"
            elif len(self.h1) >= 20 or len(self.h1) <= 70:
                return "correct length"
            else:
                return "long"

    def responsive_check(self):
        """
        Check if the website is responsive
        Args:
        html (str): html content of the website
        Returns:
        int: score
        list: message
        """
        x = self.soup
        html = self.html
        # get meta viewport tag value
        message = []
        score = 0
        if (
            str(x.find("meta", {"name": "viewport"}).get("content"))
            == "width=device-width, initial-scale=1.0"
        ):
            score += 10
            message.append("Meta viewport tag is set correctly")
        # check if there are media queries in the html
        if "@media" in html:

            score += 10
            message.append("Media queries are present")
        if "max-width" in html:
            score += 10
            message.append("Max-width is present")

        results = {
            "score": score,
            "message": message,
        }

        return results

    def searchengine_check(self):
        """
        Check if the website is search engine friendly
        Args:
        html (str): html content of the website
        Returns:
        int: score
        list: message
        """
        soup = self.soup
        # get meta viewport tag value
        message = []
        score = 0
        # check if there are meta description tag
        if soup.find("meta", {"name": "description"}):
            score += 10
            message.append("Meta description tag is present")
        # check if page has H1 tag
        if soup.find("h1"):
            score += 10
            message.append("H1 tag is present")

        results = {
            "score": score,
            "message": message,
        }
        return results

    def analyze_title(self):
        """
        Analyze the title of the website
        Args:
        url (str): url of the website
        html (str): html content of the website
        Returns:
        str: title of the website
        """
        if self.title is None:
            self.title = ""
        if self.title:

            if len(self.title) == 0:
                return "empty"
            elif len(self.title) > 0 or len(self.title) <= 29:
                return "short"
            elif len(self.title) >= 30 or len(self.title) <= 60:
                return "correct length"
            else:
                return "long"

    def audit_results(self):
        """
        Run all checks on the website
        Args:
        html (str): html content of the website
        Returns:
        dict: results of all checks
        """
        results = {
            "responsive": self.responsive_check(),
            "searchengine": self.searchengine_check(),
            "title": self.analyze_title(),
            "meta_description": self.analyze_meta_description(),
            "h1": self.analyze_H1(),
        }
        return results


# import requests

# url = "https://prasannakulkarni.com/"
# response = requests.get(url)
# html = response.text
# web = Webpage(url=url, html=html)
# __ = web.extract_text()
# _ = web.json_html()
# print(__)
