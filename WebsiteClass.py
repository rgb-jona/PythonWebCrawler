try:
    import requests
except ImportError:
    raise ImportError("Module requests could not be imported")

# todo: check for more ending signs of a url like "/ " or "/>" or ";"
#       add support for a database like mongodb
class WebsiteClass:
    """This is a simple website class to store the data of the webcrawler results"""
    def __init__(self, url):
        self.__url = url


    def CrawlWebsite(self):
        """This is the main function of the class which extracts the urls from its html text"""
    # prepare text of the webpage for crawling
        # get html response
        try:
            htmlResponseTextString = requests.get(self.__url)
        except Exception as e:
            print(e,end='')
            return []

        # split up the html text string into the single lines
        htmlTextLinesList = htmlResponseTextString.text.split('\n')

    # search for urls in webpage
        # prepare list for webpages which could be found on the website
        foundUrlList = []

        # searching wor ulrs in every line of the webpage
        for line in htmlTextLinesList:
            # search for http string appearance in line
            httpStringIndexList = self.RecursiveSearch(line,'https://')

            # search for endings of the https strings
            endingIndexList = self.RecursiveSearch(line,'"')

            if httpStringIndexList and endingIndexList:
                # find correct ending index for every string in line, beginning with "http"
                for httpStringIndex in httpStringIndexList:
                    # searching for ending with closest distance to httpStringIndex but index greater than httpStringIndex
                    indexDistanceList = [endingIndex-httpStringIndex for endingIndex in endingIndexList if endingIndex-httpStringIndex > 0]

                    if indexDistanceList:
                        endingIndex = indexDistanceList[0] + httpStringIndex
                        foundUrl = line[httpStringIndex:endingIndex]
                        if self.CheckIfUsefulUrl(foundUrl):
                            foundUrlList.append(WebsiteClass(foundUrl))

        return foundUrlList


    def CheckIfUsefulUrl(self,url):
        """This function checks if the url leads to any non hmtl elements like png or ico data"""
        notInUrlList = ['.ico','.js','.png','.svg','.jpg','google','.gif','twitter','guidestar','.css','.xml','.iso','.tar','.zip'
                        ,'.7z','.gz','.doc','docx','.mp4','.mp3','.mpeg','.pdf','.avi']
        for definedString in notInUrlList:
            if definedString in url:
                return []
        return url


    def GetUrl(self):
        return self.__url


    def RecursiveSearch(self, string, searchString):
        """This function returns all appearances of searchString in string and returns them as list"""
        stringIndex = string.find(searchString)
        if stringIndex >= 0:
            # search for further appearances of searchString in string by recursively calling the RecursiveSearch function
            # with trimmed string from stringIndex+1 to end to prevent finding same string position as before again
            resultList = self.RecursiveSearch(string[stringIndex+1:],searchString)

            # since the string was trimmed the stored indices need to be corrected
            for counter in range(0,len(resultList)):
                resultList[counter] += stringIndex+1

            # insert is used instead of append to ensure that the indices are sorted from lowest to highest value
            resultList.insert(0,stringIndex)
            return resultList
        else:
            # returning empty array so it can be filled with the results of the function calls before
            return []
