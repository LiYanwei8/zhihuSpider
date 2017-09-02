# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from utils.common import extract_num
from settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT

class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class ZhihuQuestionItem(scrapy.Item):
    #知乎的问题 item
    # id
    zhihu_id = scrapy.Field()
    # 主题
    topics = scrapy.Field()
    # url
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 回答数
    answer_num = scrapy.Field()
    # 评论数
    comments_num = scrapy.Field()
    # 浏览数
    watch_user_num = scrapy.Field()
    # 点击
    click_num = scrapy.Field()
    # 爬取时间
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        #插入知乎question表的sql语句 ON DUPLICATE KEY UPDATE防止重复出入
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        # 转换成字符串
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)

        return insert_sql, params



class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    # id
    zhihu_id = scrapy.Field()
    # url
    url = scrapy.Field()
    # id
    question_id = scrapy.Field()
    # 用户ID
    author_id = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 点赞
    praise_num = scrapy.Field()
    # 评论
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    print praise_num

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
              update_time=VALUES(update_time)
        """
        # int 类型 转换成 datetime 类型 在转换成字符串类型
        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)

        print '答案插入'
        print self["zhihu_id"]
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params


class UserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    #id
    user_id = scrapy.Field()
    #头像img
    user_image_url = scrapy.Field()
    #姓名
    name = scrapy.Field()
    #居住地
    location = scrapy.Field()
    #技术领域
    business = scrapy.Field()
    #性别
    gender = scrapy.Field()
    #公司
    employment = scrapy.Field()
    #职位
    position = scrapy.Field()
    #教育经历
    education = scrapy.Field()
    #我关注的人数
    followees_num = scrapy.Field()
    #关注我的人数
    followers_num = scrapy.Field()

class RelationItem(scrapy.Item):
    #用户id
    user_id =scrapy.Field()
    #relation 类型
    relation_type =scrapy.Field()
    #和我有关系人的id列表
    relations_id = scrapy.Field()
