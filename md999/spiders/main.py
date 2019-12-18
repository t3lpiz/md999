# -*- coding: utf-8 -*-
import scrapy
from csv import DictWriter
from urllib.request import urlopen
from lxml import html
import re

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['999.md']
    start_urls = ['https://999.md/ru/list/phone-and-communication/radio']

    def parse(self, response):
        linkuri_anunturi = response.xpath('//a[contains(@href, "ru")]/@href').getall()
        for link in linkuri_anunturi:
            if len(link) == 12:
                yield scrapy.Request(url="http://999.md" + link, callback=self.parse_links)
        #self.next_page()
        next_p = response.xpath('//ul/li/a[contains(@href, "radio?page=")]/@href').get()
        yield scrapy.Request(url="http://999.md" + next_p, callback=self.parse)


    def parse_links(self, response):
        items = {}
        phones = []
        fieldnames = ['name', 'description', 'price']
        names = response.xpath('//h1[@itemprop="name"]/text()' ).getall()
        descriptions = response.xpath('//div[@itemprop="description"]/text()').getall()
        prices = response.xpath('//span[@itemprop="price"]/text()').getall()
        tree = html.fromstring(urlopen(response.url).read())
        phones_all = tree.xpath('//a[@href]')
        #for el in phones_all:
        #    searched_el = "tel+373"
        #    match = re.search(searched_el, el.get('href')
        #            )
        #    if match:
        #        phones.append(el.get('href'))
        for name, description, price in zip(names, descriptions, prices):
            items['name'] = name
            items['description'] = description
            items['price'] = price
            #items['phone'] = phone
            yield items
            with open('resultat.csv', 'a') as f:
                csvwriter = DictWriter(f, fieldnames=fieldnames)
                csvwriter.writerow(items)
                f.close()

