class ScraperData(object):
    # This class is used to store data captured from the spiders. 
    # Scrapy provides no way to do this automatically without writing the data to a file.
    data = {}

    @staticmethod
    def add_data(new_data):
        ScraperData.data = {**ScraperData.data, **new_data}

    @staticmethod
    def get_data():
        return ScraperData.data.values()