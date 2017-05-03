# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SafetyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = Field()
    time = Field()
    ac_type = Field()
    operator = Field()
    registration = Field()
    carrierNumber = Field()
    first_flight = Field()
    crew_fatalities = Field()
    passengers_fatalities = Field()
    total_fatalities = Field()
    airplane_damage = Field()
    airplane_fate = Field()
    location = Field()
    phase = Field()
    nature = Field()
    departure_airport = Field()
