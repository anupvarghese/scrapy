# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SafetyItem(Item):
    # # define the fields for your item here like:
    # # name = scrapy.Field()
    Date = Field()
    Time = Field()
    Type = Field()
    Operator = Field()
    Registration = Field()
    CarrierNumber = Field()
    FirstFlight = Field()
    Engines=Field()
    TotalAirFrameHrs=Field()
    Crew = Field()
    Passengers = Field()
    TotalFatalities = Field()
    AirplaneDamage = Field()
    AirplaneFate = Field()
    Location = Field()
    Phase = Field()
    Nature = Field()
    DepartureAirport = Field()
    DestinationAirport = Field()
    FlightNumber= Field()
    Cycles=Field()
    GroundCasualities=Field()
    CollisionCasualties=Field()
    OperatingFor=Field()
    CrashSiteElevation=Field()
    OperatedBy=Field()
