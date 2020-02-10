"""This crawler class helps to encapsulate the process of the webcrawler"""

import sys
from .WebsiteClass import WebsiteClass


class CrawlerClass:
    crawledWebpages = []

    def __init__(self,startWebpage):
        # put start website into array which stores the websites to crawl
        self.__websitesToCrawl = [WebsiteClass(startWebpage)]

        # start crawling the websites
        self.CrawlWebsites()

    def CrawlWebsites(self):
        """takes a object of type WebsiteClass from the websitesToCrawl list and search for new urls while there are alements
        in the websitesToCrawl list"""
        print('=====Crawling Webpages=====')
        while self.__websitesToCrawl:
            actualWebsiteToCrawl = self.__websitesToCrawl.pop()
            if actualWebsiteToCrawl.GetUrl() not in CrawlerClass.crawledWebpages:
                print("crawling %s" %actualWebsiteToCrawl.GetUrl(),end='')
                CrawlerClass.crawledWebpages.append(actualWebsiteToCrawl.GetUrl())
                try:
                    foundUrlsList = actualWebsiteToCrawl.CrawlWebsite()
                    self.__websitesToCrawl += foundUrlsList
                    print(" .....OK, found %d Urls" % len(foundUrlsList))
                except RecursionError:
                    print(" .....Recursion error")
