import scrapy
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
        columns = hxs.xpath("//td")
        keys = columns[::2]
        vals = columns[1::2]
        columns = hxs.xpath("//span")
        print '******************START*************'
        item = {}
        for key, val in zip(keys, vals):
            item_key = key.css('.caption::text').extract()
            item_vals = val.css('.desc')
            item_text = val.css('.desc::text').extract()
            item_val = item_text
            if len(item_text) < 1:
                for val in item_vals:
                    item_val = val.css("a::text").extract()
            if len(item_key) > 0 and item_key[0][:-1].strip() == 'Date':
                item_val = val.css('.caption::text').extract()
            if len(item_key) > 0 and item_key[0][:-1].strip() == 'Location':
                location = str(val.css("a::text").extract()[
                    0]) + ' / ' + str(val.css('.desc::text').extract()[0][:-1].strip())
                item_val = [location]

            if len(item_key) > 0 and len(item_val) > 0:
                nice_key = str(item_key[0])[:-1].strip()
                nice_val = str(item_val[0]).strip().replace(
                    ',', '#').replace('=', '#')
                aviation_item['FlightNumber'] = '-'
                aviation_item['Cycles'] = '-'
                aviation_item['GroundCasualities'] = '-'
                aviation_item['CollisionCasualties'] = '-'
                aviation_item['OperatingFor'] = '-'
                aviation_item['CrashSiteElevation'] = '-'
                aviation_item['OperatedBy'] = '-'
                aviation_item['DestinationAirport'] = '-'
                if 'C/n / msn' in nice_key:
                    nice_key = 'CarrierNumber'
                if 'Flightnumber' in nice_key:
                    nice_key = 'FlightNumber'
                if 'First flight' in nice_key:
                    nice_key = 'FirstFlight'
                if 'Total airframe hrs' in nice_key:
                    nice_key = 'TotalAirFrameHrs'
                if 'Crew' in nice_key:
                    nice_key = 'Crew'
                if 'Passengers' in nice_key:
                    nice_key = 'Passengers'
                if 'Total' in nice_key:
                    nice_key = 'TotalFatalities'
                if 'Airplane damage' in nice_key:
                    nice_key = 'AirplaneDamage'
                if 'Airplane fate' in nice_key:
                    nice_key = 'AirplaneFate'
                if 'Location' in nice_key:
                    nice_key = 'Location'
                if 'Departure airport' in nice_key:
                    nice_key = 'DepartureAirport'
                if 'Ground casualties' in nice_key:
                    nice_key = 'GroundCasualities'
                if 'Collision casualties' in nice_key:
                    nice_key = 'CollisionCasualties'
                if 'Operating for' in nice_key:
                    nice_key = 'OperatingFor'
                if 'Operating for' in nice_key:
                    nice_key = 'CrashSiteElevation'
                if 'Cycles' in nice_key:
                    nice_key = 'Cycles'
                if 'Operated by' in nice_key:
                    nice_key = 'OperatedBy'
                if 'Destination airport' in nice_key:
                    nice_key = 'DestinationAirport'
                aviation_item[nice_key] = nice_val
        print '******************END*************'
        return aviation_item
