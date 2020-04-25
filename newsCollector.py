import newsProvider

if __name__ == '__main__':
    links = newsProvider.NewsProvider("Apple stock", 5)
    print(links.getNews())
