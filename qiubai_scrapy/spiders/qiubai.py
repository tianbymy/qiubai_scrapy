# -*- coding: utf-8 -*-
import scrapy
from qiubai_scrapy.items import QiubaiItem
from scrapy.http import Request
import logging

class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['qiushibaike.com']
    host = 'https://www.qiushibaike.com'
    protocol = 'https:'
    start_urls = [
        '',             # 主页
        'hot/',          # 24小时
        'imgrank/',      # 热图
        'text/',         # 文字
        'history/',      # 穿越
        'pic/',          # 糗图
        'textnew/'       # 新鲜
    ]
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='qiubai.log',
        filemode='w')

    def start_requests(self):
        for type in self.start_urls:
            yield Request(url=self.host + '/%s' % type, callback=self.parse)

    def parse(self, response):
        logging.debug('request url:------>' + response.url)
        # 段子
        for block in response.xpath('//div[@class="col1"]/div'):
            # uuid
            uuid = block.xpath('@id').extract_first()

            # 作者
            author_block = block.xpath('div[@class="author clearfix"]')
            name = author_block.xpath('a[2]/h2/text()').extract_first()
            avatar = author_block.xpath('a[1]/img/@src').extract_first()

            # 匿名
            if name is None:
                name = author_block.xpath('span[2]/h2/text()').extract_first()
            if avatar is None:
                avatar = author_block.xpath('span[1]/img/@src').extract_first()

            if name is not None:
                name = name.strip('\n')
            if avatar is not None and avatar.startswith(self.protocol) is not True:
                avatar = self.protocol + avatar




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

            if thumb is not None and thumb.startswith(self.protocol) is not True:
                thumb = self.protocol + thumb


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
        next_page = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').extract_first()
        if next_page is not None:
            url = self.host + '%s' % next_page
            logging.debug(' next page:---------->' + url)
            yield Request(url=url, callback=self.parse)