from event_processor.base.custom_spiders import ScraperSpider

# For individuals they have a process of contacting somebody https://www.thenightministry.org/individual-direct-service-next-steps-page
# ... but they also have individual event calender for fundraising
# https://www.thenightministry.org/events

class NightMinistrySpider(ScraperSpider):
    name = 'nightministry'
    allowed_domains = ['thenightministry.org'] 
    enabled = True

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'The Night Ministy', 'https://www.thenightministry.org/', date_format='%Y', **kwargs)

    def start_requests(self):
        yield self.get_request('events/', {})

    def parse(self, response): 
        print("Parsing page...") 
        def index_from_br_split(txt, x, altx=x): # string, index
            spl = txt.split("<br>")
            try:
                t = spl[x]
                return t
            except IndexError:
                try: 
                    t = spl[altx]
                    return t
                except IndexError:
                    return ''
        
        return {
            'title': self.empty_check_extract(response.css('.el-item'), self.css_func, '.el-title::text'), 
            'url': self.empty_check_extract(response.css('.el-item'), self.css_func, '.el-link::text'), 
            'event_time': self.create_time_data(
                date=list(map(lambda txt: index_from_br_split(txt, 0), self.empty_check_extract(response.css('.el-item'), self.css_func, '.el-content p::text'))),
                time_range=list(map(lambda txt: index_from_br_split(txt, 1), self.empty_check_extract(response.css('.el-item'), self.css_func, '.el-content p::text')))
            ),
            'address': list(map(lambda txt: index_from_br_split(txt, 3, 2), self.empty_check_extract(response.css('.el-item'), self.css_func, '.el-content p::text'))),
            'description': self.empty_check_extract(response.css('.el-item'), self.css_func, '.el-title::text')
        }
