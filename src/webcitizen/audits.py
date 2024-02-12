# open file
import bs4

from webpage import WebPage


class Audit(WebPage):

    # TODO: Audit canonical

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

    def responsive_check(self, html: str):
        """
        Check if the website is responsive
        Args:
        html (str): html content of the website
        Returns:
        int: score
        list: message
        """
        x = bs4.BeautifulSoup(html, "html.parser")
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

        return score, message

    def searchengine_check(self, html: str):
        """
        Check if the website is search engine friendly
        Args:
        html (str): html content of the website
        Returns:
        int: score
        list: message
        """
        x = bs4.BeautifulSoup(html, "html.parser")
        # get meta viewport tag value
        message = []
        score = 0
        # check if there are meta description tag
        if x.find("meta", {"name": "description"}):
            score += 10
            message.append("Meta description tag is present")
        # check if page has H1 tag
        if x.find("h1"):
            score += 10
            message.append("H1 tag is present")

        return score, message

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
