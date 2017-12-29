# -*- coding: utf-8 -*-
import scrapy
from qiubai_scrapy.items import QiubaiItem

class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        # 段子
        for block in response.xpath('//div[@class="col1"]/div'):
            # uuid
            uuid = block.xpath('@id').extract_first()

            # 作者
            author_block = block.xpath('div[@class="author clearfix"]')
            name = author_block.xpath('a[2]/h2/text()').extract_first().strip('\n')
            avatar = author_block.xpath('a[1]/img/@src').extract_first()
            if author_block.xpath('div[@class="articleGender manIcon"]').extract_first() is not None:
                gender = 'man'
                age = author_block.xpath('div[@class="articleGender manIcon"]/text()').extract_first()
            elif author_block.xpath('div[@class="articleGender womenIcon"]').extract_first() is not None:
                gender = 'woman'
                age = author_block.xpath('div[@class="articleGender womenIcon"]/text()').extract_first()
            else:
                gender = 'unknown'
                age = 'unknown'

            # 内容（暂未处理图片）
            content_block = block.xpath('a[@class="contentHerf"]')
            content = ''.join(content_block.xpath('div/span/text()').extract()).strip('\n')

            thumb_block = block.xpath('div[@class="thumb"]')
            thumb = thumb_block.xpath('a/@src').extract_first()

            # 其他
            stats_block = block.xpath('div[@class="stats"]')
            vote = stats_block.xpath('span[@class="stats-vote"]/i/text()').extract_first()
            comment = stats_block.xpath('span[@class="stats-comments"]/a/i/text()').extract_first()

            #
            item = QiubaiItem()
            item['uuid'] = uuid
            item['name'] = name
            item['avatar'] = avatar
            item['gender'] = gender
            item['age'] = age
            item['content'] = content
            item['thumb'] = thumb
            item['vote'] = vote
            item['comment'] = comment
            yield item

            # 下一页
            # next_page = response.xpath('//ul[@class="pagination"]/li[last()]/a')
            # yield response.follow(next_page, callback=self.parse)