from base.custom_spiders import ScraperSpider

# For individuals they have a process of contacting somebody https://www.thenightministry.org/individual-direct-service-next-steps-page
# ... but they also have individual event calender for fundraising
# https://www.thenightministry.org/events

class NightMinistrySpider(ScraperSpider):
    name = 'nightministry'
    allowed_domains = ['thenightministry.org'] 

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'The Night Ministy', 'https://www.thenightministry.org/', date_format='%Y', **kwargs)

    def start_requests(self):
        yield self.get_request('events/', {})

    def parse(self, response): 
        print("Parsing page...") 
        def get_br_date(sr, ind): 
            print("sr = " + str(sr)) 
            try:
                return sr[0].split("<br>")[ind]
            except IndexError:
                return "" # not a valid split? 

        for result in response.css("div.el-item"): 
            print("**************** P A R S E   S T U F F")
            print(result) 
            yield {
                'title': result.css('.el-title::text').extract(),
                'url': result.css('.el-link::text').extract(),
                'event_time': #self.extract_multiple(
                    {'date': get_br_date(result.css('.el-content p::text').extract(), 0), 
                    'start_time': get_br_date(result.css('.el-content p::text').extract(), 1)}, # ),
                'address': get_br_date(result.css('.el-content p::text').extract(), -1),
                'description': result.css('.el-title::text').extract() # title 
            }
