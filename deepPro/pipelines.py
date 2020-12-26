# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DeepproPipeline:
    # 此种方式不好
    def process_item(self, item, spider):
        # if item.__class__.__name__ == 'DeepproItem':
        # title = item['title']
        #     status = item['status']
        #     print(title+':'+status)
        # else:
        #     content = item['content']
        #     print(content)


        print(item)

        return item
