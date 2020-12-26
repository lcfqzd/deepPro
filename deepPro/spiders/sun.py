import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DeepproItem,DeepproItemDetail

class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&type=4&page=']

    # 提取页码链接
    # link = LinkExtractor(allow=r'/political/index/politicsNewest?id=1&page=\d+')  # 错误，拼接不能重复
    # link = LinkExtractor(allow=r'id=1&page=\d+')
    link = LinkExtractor(allow=r'id=1&page=\d+')

    # /political/politics/index?id=484552
    # link_detail = LinkExtractor(allow=r'index\?id=\d+')

    rules = (
        # 解析每一个页码对应页面中的数据
        Rule(link, callback='parse_item', follow=True),

        # 对于详情页面自己手动发请求，便于进行请求传参将此页面要获取的内容携带进入详情页面整合(使用meta={'item':item})
        # Rule(link_detail, callback='parse_detail', follow=False),
    )

    # 标题&状态
    # def parse_item(self, response):
    #     #/html/body/div[2]/div[3]/ul[2]/li
    #     li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
    #     for li in li_list:
    #         title = li.xpath('./span[3]/a/text()').extract_first()
    #         status = li.xpath('./span[2]/text()').extract_first()
    #
    #         item = DeepproItem()
    #         item['title'] = title
    #         item['status'] = status
    #         print(item)
    #
    #         yield item

    # 实现深度爬取：爬取详情页中的数据
    # 1.对详情页的url进行捕获
    # 2.对详情页的url发起请求获取数据
    # def parse_detail(self,response):
    #     content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
    #     item = DeepproItemDetail()
    #     item['content'] = content
    #     print(item)
    #     yield item

    # 问题：
    # 1.爬虫文件会向管道中提交两个不同形式的item，管道会接收到两个不同形式的item
    # 2.管道如何区分两种不同形式的item
    #   -在管道中判断接收到的item到底是哪个
    # 3.持久化存储的，目前无法将title和content进行一一匹配



    def parse_item(self, response):
        # li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        # for li in li_list:
        #     title = li.xpath('./span[3]/a/text()').extract_first()
        #     status = li.xpath('./span[2]/text()').extract_first()
        #
        #     # 提取进入详情页的链接
        #     detail_url = 'http://wz.sun0769.com'+li.xpath('./span[3]/a/@href').extract_first()
        #
        #     item = DeepproItem()
        #     item['title'] = title
        #     item['status'] = status
        #     print(item)
        #
        #     yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'item':item})

        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            title = li.xpath('./span[3]/a/text()').extract_first()
            status = li.xpath('./span[2]/text()').extract_first()
            detail_url = 'http://wz.sun0769.com' + li.xpath('./span[3]/a/@href').extract_first()
            item = DeepproItem()
            item['title'] = title
            item['status'] = status

            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self,response):
        item = response.meta['item']
        content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
        item['content'] = content

        yield item