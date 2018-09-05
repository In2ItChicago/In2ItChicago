import scrapy
from scrapy.spiders import Spider
from event import Event
from event import EventFieldData
from categories import Category
from spider_base import SpiderBase
import pprint

class LakeviewPantry(Spider, SpiderBase):
    name = 'lakeview_pantry'
    allowed_domains = ['www.lakeviewpantry.org']
    start_urls = ['http://www.lakeviewpantry.org/events-2.html']

    #needed for AggregatorBase initialization.
    def __init__(self, start_date, end_date):
        SpiderBase.__init__(self, 'www.lakeviewpantry.org', start_date, 
        	end_date, date_format = '%W, %M %e, %Y')

    def parse(self, response):

        #we have html that looks like this:
        """
        '<div class="textwidget">
            <p>*Please arrive on time for volunteer orientations. If you are more than 15 minutes late, you may be asked to attend another session. Anyone under 18 years old must complete a youth waiver, have a parent/guardian present during the orientation and both must be registered on our website. Thank you! 
            </p>\n
            <p><strong> Thursday, August 23</strong>
                <br>\n11:00AM - 12:00PM
                <br>\nVolunteer Orientation Session
                <br>\nLakeview Pantry Sheridan
                <br>\n3945 N. Sheridan
            </p>\n
            <p><strong> Wednesday, August 29</strong><br>\n6:00PM - 7:00PM<br>\nVolunteer Orientation Session<br>\nLakeview Pantry Sheridan<br>\n3945 N. Sheridan</p>\n<p><strong> Thursday, September 6</strong><br>\n11:00AM - 12:00PM<br>\nVolunteer Orientation Session<br>\nLakeview Pantry Sheridan<br>\n3945 N. Sheridan</p>\n<p><strong> Tuesday, September 11</strong><br>\n6:00PM - 7:00PM<br>\nVolunteer Orientation Session<br>\nLakeview Pantry Sheridan<br>\n3945 N. Sheridan</p>\n<p><strong> Saturday, September 15</strong><br>\n2:00PM - 3:00PM<br>\nVolunteer Orientation Session<br>\nLakeview Pantry Sheridan<br>\n3945 N. Sheridan</p>\n<p><strong> Thursday, September 20</strong><br>\n11:00AM - 12:00PM<br>\nVolunteer Orientation Session<br>\nLakeview Pantry Sheridan<br>\n3945 N. Sheridan</p>\n<p><strong> Tuesday, September 25</strong><br>\n6:00PM - 7:00PM<br>\nVolunteer Orientation Session<br>\nLakeview Pantry Sheridan<br>\n3945 N. Sheridan</p>\n</div>', '<div class="textwidget"><p>Our mission is to eliminate hunger in our community by: providing food to fill the basic need of hungry people, increasing the independence of our clients through self-help initiatives and other innovative programs, and raising awareness of hunger and poverty and working towards solutions to eliminate them.</p>\n</div>', '<div class="textwidget"><p>Lakeview Pantry Sheridan location<br>\n3945 N. Sheridan Rd.<br>\nChicago, IL 60613<br>\n(773) 525 1777</p>\n<p>*Please note: You can NOT park in the Walgreens lot next to the Sheridan site. If you do, you will be towed! There is free loading zone parking in front of our building. Use hazard lights when parking there. </p>\n<p>Lakeview Pantry Oakdale location<br>\n1414 W. Oakdale Ave.<br>\nChicago, IL 60657<br>\n(773) 525 1777</p>\n</div>', '<div class="textwidget"><p>Lakeview Pantry Sheridan location<br>\nMonthly Food Distribution Hours:<br>\nMon, Wed, Fri: 12 - 4 pm<br>\nThursday: 4-7 pm</p>\n<p>Weekly Produce Pick-up Hours:<br>\nMon, Wed, Fri: 2 - 4 pm<br>\nThursday: 4 - 7 pm</p>\n<p>Donation Drop-Off<br>\nMon - Fri: 9 - 5 pm  </p>\n<p>Lakeview Pantry Oakdale location<br>\nMonthly and Weekly Food Distribution Hours:<br>\nTu, Thu: 6 - 8 pm;<br>\nSat: 11:30 am - 1:30 pm </p>\n<p>Donation Drop-Off<br>\nTu, Thu: 4:30 - 7 pm;<br>\nSat: 10 am - 1 pm;<br>\nOr call in advance</p>\n</div>', '<div class="textwidget"><p>OUR SHERIDAN SITE WILL BE CLOSED IN OBSERVANCE OF LABOR DAY- MONDAY, SEPTEMBER 3RD.</p>\n<p>OUR OAKDALE SITE WILL BE CLOSED ON SAT, SEPTEMBER 1ST FOR LABOR DAY WEEKEND AND CLOSED SAT, SEPTEMBER 29TH DUE TO A STREET FESTIVAL. </p>\n</div>'
        """

        base_selector = response.css('.textwidget') #has all of textwidget. [0] will be our place.
        first_widget_selector = base_selector[0] #select first result, has all our dates.
        paragraphs_only = first_tw_selector.xpath('.//p') #select only ps. 

        #initialize our lists to add to as we traverse our paragraphs.
        dates = []
        times = []
        titles = []
        descriptions = []
        addresses = []
        urls = []

        #traverse paragraphs from index=1 to end.  these start with date.
        for i in range(1,len(paragraphs_only)): #only traverse from 1 - end.
            curr_parag = paragraphs_only[i].extract() #works well, gives entire p
            string_vals = curr_parag.split('<br>\n')#split on breaks.
            #now inserting to our lists:
            dates.append(string_vals[0].replace('<p><strong> ','').replace('</strong>',''))
            times.append(string_vals[1].replace(' ', ''))
            titles.append(string_vals[2])
            descriptions.append('')
            addresses.append(string_vals[4].replace('</p>',''))
            urls.append('http://www.lakeviewpantry.org/events-2.html')
            #done.

        #convert lists to EventFieldData type:
        title_efd = EventFieldData('title',titles)
        time_efd = EventFieldData('time_range', times)
        date_efd = EventFieldData('date', dates)
        address_efd = EventFieldData('address', addresses)
        description_efd = EventFieldData('description', descriptions)
        urls_efd = EventFieldData('url', urls)
        #return info.
        return self.create_events('Lakeview Food Pantry', title_efd, time_efd, date_efd, address_efd, description_efd, urls_efd)
