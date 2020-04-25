import regex as re
import requests
from bs4 import BeautifulSoup
import time
import datetime
import preprocessor


class NewsProvider:
    def __init__(self, searchItem, number):
        self.searchItem = searchItem
        self.number = number

    def getGoogleLinks(self):
        links = []
        url = 'https://news.google.com/rss/search?q={}'.format(self.searchItem)
        try:
            html = requests.get(url)
            if html.status_code == 200:
                soup = BeautifulSoup(html.text, 'lxml')
                items = soup.find_all(['pubdate', 'description'])

                for x in range(2, len(items), 2):
                    date = items[x - 1].text
                    timestamp = time.mktime(
                        datetime.datetime.strptime(str(date), "%a, %d %b %Y %H:%M:%S %Z").timetuple())
                    des = items[x].text
                    des = BeautifulSoup(des, 'lxml')
                    a = des.find_all('a')
                    link = a[0].get('href')
                    links.append((timestamp, link))
        except Exception as ex:
            print(str(ex))
        finally:
            return links

    def getNews(self):
        links = self.getGoogleLinks()
        print(len(links))
        news = {}
        for item in range(self.number):
            # Get the text of article
            date = int(links[item][0])
            news[date] = {}
            link = links[item][1]
            article = requests.get(link)
            soup = BeautifulSoup(article.text, "html.parser")
            for script in soup(["script", "style", "meta", "noscript"]):
                script.extract()  # rip it out
            text = soup.get_text()
            # Get the source
            source_1 = re.search('\.\\s*([^.]*)', link).group(1)
            source_2 = re.search('//\\s*([^.]*)', link).group(1)
            if "/" in source_1:
                source = source_2
            else:
                source = source_1
            news[date]['source'] = source
            news[date]['text'] = preprocessor.Preprocessor(text).preprocessData()
        return news
