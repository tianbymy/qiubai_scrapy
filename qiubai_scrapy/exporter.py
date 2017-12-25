# -*- coding: utf-8 -*-

from scrapy.exporters import JsonLinesItemExporter

class CustomJsonLinesItemExporter(JsonLinesItemExporter):

    def __init__(self, file, **kwargs):
        super(CustomJsonLinesItemExporter, self).__init__(file, ensure_ascii=False, **kwargs)
