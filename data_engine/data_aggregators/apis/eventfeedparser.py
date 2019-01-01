import feedparser

class EventFeedparser:
    def __init__(self, url):
        self.feed = feedparser.parse(url)