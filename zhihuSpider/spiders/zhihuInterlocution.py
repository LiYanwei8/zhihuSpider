# -*- coding: utf-8 -*-
import scrapy
import re
import json
from PIL import Image
from fake_useragent import UserAgent
try:
    import urlparse as parse
except:
    from urllib import parse
from scrapy.loader import ItemLoader
from zhihuSpider.items import ZhihuQuestionItem, ZhihuAnswerItem
import datetime

class ZhihuinterlocutionSpider(scrapy.Spider):
    name = 'zhihuInterlocution'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    # question的第一页answer的请求url json
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    ua = UserAgent()
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': ua.random
    }
    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数

        """

        all_urls = response.xpath("//a/@href").extract()
        # parse生成链接
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 过滤javascrip
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            # 两种url
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                print "你好世界 "
                print request_url
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:

                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        #处理question页面， 从页面中提取出具体的question item

        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        if match_obj:
            question_id = int(match_obj.group(2))

        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_xpath("title", ".//*[@class='QuestionHeader-title']/text()")
        item_loader.add_xpath("content", ".//*[@class='QuestionHeader-detail']")
        item_loader.add_value("url", response.url)
        item_loader.add_value("zhihu_id", question_id)
        item_loader.add_xpath("answer_num", ".//*[@class='List-headerText']/span/text()")
        item_loader.add_xpath("comments_num", ".//*[@class='QuestionHeader-Comment']/button/text()")
        # 有两个 但是是button 加载后才出现的 后面作处理
        item_loader.add_xpath("watch_user_num", ".//*[@class='NumberBoard-value']/text()")
        item_loader.add_xpath("topics", ".//*[@class='QuestionHeader-topics']//*[@class='Popover']//text()")

        question_item = item_loader.load_item()

        # 发送答案请求
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0),
                             headers=self.headers,
                             callback=self.parse_answer)
        yield question_item


    # 点击更多获取 api接口
    def parse_answer(self, reponse):
        #处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]
        print next_url
        #提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url,
                                 headers=self.headers,
                                 callback=self.parse_answer)


    def start_requests(self):
        # 登录知乎
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]


    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))
        print xsrf
        if xsrf:
            #     post_url = "https://www.zhihu.com/login/email"
            #     post_data = {
            #         "_xsrf": _xsrf,
            #         "email": account,
            #         "password": password,
            #         "captcha": text
            # }
            # zhihu_login("18782902568", "admin123")
            # zhihu_login("1575985731@qq.com", "Qianfeng008")

            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": xsrf,
                "email": "1575985731@qq.com",
                "password": "Qianfeng008",
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url,
                                 headers=self.headers,
                                 meta={"post_data": post_data},
                                 callback=self.login_after_captcha)


    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        try:
            im = Image.open('captcha.jpg')
            im.show()
            # im.close()
        except:
            pass

        captcha = raw_input('输入验证码：')

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/email"
        posturl = response.meta.get("url", {})
        print posturl
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]


    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        print text_json
        if "msg" in text_json and text_json["msg"] == u"登录成功":
            print "登录成功"
            # 延后执行
            for url in self.start_urls:
                # 默认跳转parse函数
                yield scrapy.Request(url,
                                     # 不过滤
                                     dont_filter=True,
                                     headers=self.headers)
        else:
            print "登录失败"