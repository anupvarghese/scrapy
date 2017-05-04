# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from csv import DictWriter

class SafetyPipeline(object):
    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, 'NULL')
        return item
