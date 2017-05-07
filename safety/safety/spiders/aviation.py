import scrapy
import sys
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy import Selector
from safety.items import SafetyItem

"""
Class to scrap https://aviation-safety.net/database/
"""


class AviationSpider(CrawlSpider):
    """Spider"""
    name = "aviation"
    allowed_domains = ["https://aviation-safety.net/database/dblist",
                       "https://aviation-safety.net/database/record"]

    """
    start requests
    """

    def start_requests(self):
        """Begin firing requests"""
        urls = [
            'https://aviation-safety.net/database',
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)
    """
    method to get url
    """

    def find_url(self, filter, title):
        """Gets the url"""
        link = ''

        link = title.css('a::attr(href)')[0].extract()
        if filter in link:
            link = title.xpath("@href")[0].extract()
            withdb = link.strip().split('/')
            if withdb[0] == '':
                withdb = withdb[1:]
            if withdb[0] == 'database':
                withoutdb = withdb[1:]
                link = '/'.join(withoutdb)
            else:
                link = withdb[0]
            return link

    """
    parse callback
    """

    def parse(self, response):
        """First level scraping"""
        hxs = Selector(response)
        titles = hxs.xpath("//a")
        filter = 'dblist.php'
        item = SafetyItem()

        for title in titles:
            link = self.find_url(filter=filter, title=title)
            if link:
                url = 'https://aviation-safety.net/database/' + link
                request = Request(
                    url=url, callback=self.parse_second_page, dont_filter=True)
                request.meta['item'] = item
                yield request

    """
    parse callback for second page scrapping
    """

    def parse_second_page(self, response):
        """Second level scraping"""
        item = response.meta['item']
        hxs = Selector(response)
        titles = hxs.xpath("//a")
        filter = 'record.php'
        for title in titles:
            link = self.find_url(filter=filter, title=title)
            if link:
                request = Request(
                    url='https://aviation-safety.net/database/' +
                    link, callback=self.parse_third_page, dont_filter=True)
                request.meta['item'] = item
                yield request

    """
    parse callback for second page scrapping
    """

    def parse_third_page(self, response):
        """Third level scraping"""
        aviation_item = response.meta['item']
        hxs = Selector(response)
        # for row in rows:
        rows = hxs.xpath("//tr//td")
        key_columns = rows[::2]
        val_columns = rows[1::2]

        for key, val in aviation_item.iteritems():
            if val is not None:
                aviation_item[key] = '-'

        for key, val in zip(key_columns, val_columns):
            a_texts = val.xpath("a/text()").extract()
            key_text = key.xpath("./text()").extract()
            if len(key.xpath("./nobr/text()").extract()):
                key_text = key.xpath("./nobr/text()").extract()
            val_text = val.xpath("./text()").extract()
            narratives = val.xpath("//span/text()").extract()
            nice_key = ''
            nice_val = ''
            narrative = ''
            # print val_text, key_text, '2'
            if len(key_text) > 0:
                nice_key = key_text[0].encode('utf-8')
            if len(val_text) > 0:
                nice_val = val_text[0].encode('utf-8')
                # print nice_val, key_text, '1'
            if len(a_texts) > 0:
                for item_text in a_texts:
                    nice_val += item_text.encode('utf-8')
            if len(narratives) > 1:
                narrative = narratives[1]

            nice_key = nice_key.strip()
            # print nice_val, nice_key, '2'
            if nice_key == '':
                continue

            # print nice_val, nice_key, '3'

            if nice_key.lower().find('type') > -1:
                nice_key = 'Type'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('registration') > -1:
                nice_key = 'Registration'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('engines') > -1:
                nice_key = 'Engines'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('operator') > -1:
                nice_key = 'Operator'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('date') > -1:
                nice_key = 'Date'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('phase') > -1:
                nice_key = 'Phase'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('nature') > -1:
                nice_key = 'Nature'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('time') > -1:
                nice_key = 'Time'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('status', 0) > -1:
                # print 'wTF', nice_val
                nice_key = 'Status'
                aviation_item[nice_key] = nice_val
                # print aviation_item['Status'], 'real fuck'
            elif nice_key.lower().find('c/n / msn') > -1:
                nice_key = 'CarrierNumber'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('flightnumber') > -1:
                nice_key = 'FlightNumber'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('first flight') > -1:
                nice_key = 'FirstFlight'
                aviation_item[nice_key] = nice_val

            elif nice_key.lower().find('total airframe hrs') > -1:
                nice_key = 'TotalAirFrameHrs'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('crew') > -1:
                nice_key = 'Crew'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('passengers') > -1:
                nice_key = 'Passengers'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('total') > -1:
                nice_key = 'TotalFatalities'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('airplane damage') > -1:
                nice_key = 'AirplaneDamage'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('airplane fate') > -1:
                nice_key = 'AirplaneFate'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('location') > -1:
                nice_key = 'Location'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('departure airport') > -1:
                nice_key = 'DepartureAirport'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('ground casualties') > -1:
                nice_key = 'GroundCasualities'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('collision casualties') > -1:
                nice_key = 'CollisionCasualties'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('operating for') > -1:
                nice_key = 'OperatingFor'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('crash site elevation') > -1:
                nice_key = 'CrashSiteElevation'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('cycles') > -1:
                nice_key = 'Cycles'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('operated by') > -1:
                nice_key = 'OperatedBy'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('destination airport') > -1:
                nice_key = 'DestinationAirport'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('on behalf of') > -1:
                nice_key = 'OnBehalfOf'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('leased from') > -1:
                nice_key = 'LeasedFrom'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('investigating') > -1:
                nice_key = 'InvestigatingAgency'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('released') > -1:
                nice_key = 'Released'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('duration of investigation') > -1:
                nice_key = 'DurationOfInvestigation'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('download report') > -1:
                nice_key = 'DownloadReport'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('duration') > -1:
                nice_key = 'Duration'
                aviation_item[nice_key] = nice_val
            elif nice_key.lower().find('issued') > -1:
                nice_key = 'Issued'
                aviation_item[nice_key] = nice_val
            aviation_item['Narrative'] = narrative
        return aviation_item
