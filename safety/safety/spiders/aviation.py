# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy import Selector
from safety.items import SafetyItem


class AviationSpider(CrawlSpider):
  name = "aviation"
  allowed_domains = ["https://aviation-safety.net/database/dblist",
                     "https://aviation-safety.net/database/record"]

  def start_requests(self):
    urls = [
      'https://aviation-safety.net/database',
    ]
    for url in urls:
      yield Request(url=url, callback=self.parse)


  def parse_again(self, response):
    item = response.meta['item']
    hxs = Selector(response)
    titles = hxs.xpath("//a")
    filter = 'record.php'

    for title in titles:
      link = title.css('a::attr(href)')[0].extract()
      if filter in link:
        link = title.xpath("@href")[0].extract()
        withdb = link.strip().split('/')
        if (withdb[0] == ''):
          withdb = withdb[1:]
        if withdb[0] == 'database' :
          withoutdb = withdb[1:]
          link = '/'.join(withoutdb)
        else:
          link = withdb[0]
        request = Request(url='https://aviation-safety.net/database/' + link, callback=self.parse3, dont_filter=True)
        request.meta['item'] = item
        yield request

  def parse3(self, response):
    aviationItem = response.meta['item']
    hxs = Selector(response)
    # for row in rows:
    columns = hxs.xpath("//td")
    keys = columns[::2]
    vals = columns[1::2]
    print '******************START*************'
    item = {}
    for key, val in zip(keys, vals):
      itemKey = key.css('.caption::text').extract()
      itemVals = val.css('.desc')
      itemText = val.css('.desc::text').extract()
      itemVal = itemText
      if (len(itemText) < 1):
        for val in itemVals:
          itemVal = val.css("a::text").extract()
      if (len(itemKey) > 0 and itemKey[0][:-1].strip() == 'Date'):
        itemVal = val.css('.caption::text').extract()
      if (len(itemKey) > 0 and itemKey[0][:-1].strip() == 'Location'):
        location = str(val.css("a::text").extract()[0]) + ' / ' + str(val.css('.desc::text').extract()[0][:-1].strip())
        itemVal = [location]

      if (len(itemKey) > 0 and len(itemVal) > 0):
        niceKey = str(itemKey[0])[:-1].strip()
        niceVal = str(itemVal[0]).strip().replace(',', '#').replace('=', '#')
        aviationItem['FlightNumber'] = '-'
        aviationItem['Cycles'] = '-'
        aviationItem['GroundCasualities'] = '-'
        aviationItem['CollisionCasualties'] = '-'
        aviationItem['OperatingFor'] = '-'
        aviationItem['CrashSiteElevation'] = '-'
        aviationItem['OperatedBy'] = '-'

        if 'C/n / msn' in niceKey:
          niceKey = 'CarrierNumber'
        if 'Flightnumber' in niceKey:
          niceKey = 'FlightNumber'
        if 'First flight' in niceKey:
          niceKey = 'FirstFlight'
        if 'Total airframe hrs' in niceKey:
          niceKey = 'TotalAirFrameHrs'
        if 'Crew' in niceKey:
          niceKey = 'Crew'
        if 'Passengers' in niceKey:
          niceKey = 'Passengers'
        if 'Total' in niceKey:
          niceKey = 'TotalFatalities'
        if 'Airplane damage' in niceKey:
          niceKey = 'AirplaneDamage'
        if 'Airplane fate' in niceKey:
          niceKey = 'AirplaneFate'
        if 'Location' in niceKey:
          niceKey = 'Location'
        if 'Departure airport' in niceKey:
          niceKey = 'DepartureAirport'
        if 'Ground casualties' in niceKey:
          niceKey = 'GroundCasualities'
        if 'Collision casualties' in niceKey:
          niceKey = 'CollisionCasualties'
        if 'Operating for' in niceKey:
          niceKey = 'OperatingFor'
        if 'Operating for' in niceKey:
          niceKey = 'CrashSiteElevation'
        if 'Cycles' in niceKey:
          niceKey = 'Cycles'
        if 'Operated by' in niceKey:
          niceKey = 'OperatedBy'
        aviationItem[niceKey] = niceVal
    return aviationItem
    print '******************END*************'


  def parse(self, response):
    hxs = Selector(response)
    titles = hxs.xpath("//a")
    filter = 'dblist.php'
    item = SafetyItem()
    link = ''
    for title in titles:
      link = title.css('a::attr(href)')[0].extract()
      if filter in link:
        link = title.xpath("@href")[0].extract()
        withdb = link.strip().split('/')
        if (withdb[0] == ''):
          withdb = withdb[1:]
        if withdb[0] == 'database' :
          withoutdb = withdb[1:]
          link = '/'.join(withoutdb)
        else:
          link = withdb[0]
        url = 'https://aviation-safety.net/database/' + link
        request = Request(url=url, callback=self.parse_again, dont_filter=True)
        request.meta['item'] = item
        yield request
