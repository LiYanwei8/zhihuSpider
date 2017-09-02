# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

import requests
import re
import time
import cPickle
import pytesseract
from PIL import Image

def save_session(session):
    '''
    将session写入文件: session.txt
    :param session:
    :return:
    '''
    with open('session.txt', 'wb') as f:
        cPickle.dump(session.headers, f)
        cPickle.dump(session.cookies.get_dict(), f)
        print '[+] 将session写入文件: session.txt'

def load_session():
    '''
    #加载session
    :return:
    '''
    with open('session.txt', 'rb') as f:
        headers = cPickle.load(f)
        cookies = cPickle.load(f)
        print '[+] 读取session.txt'
        return headers,cookies

def captcha(data):
    '''
    识别验证码
    :param data:
    :return:
    '''
    with open('captcha.jpg','wb') as fp:
        fp.write(data)
    time.sleep(1)

    try:
        image = Image.open("captcha.jpg")
        image.show()
        captcha = raw_input('输入验证码：')
        image.close()
        return captcha
    except:
        pass

    # 机器识别验证码
    # text = pytesseract.image_to_string(image)
    # print "机器识别的验证码: " + str(text)
    # command = raw_input("请输入Y表示同意使用，按其他键自行重新输入：")
    # if (command == "Y" or command == "y"):
    #     return text
    # else:
    #     return raw_input('输入验证码：')

def zhihu_login(account, password):
    '''
    知乎登录
    :param account:账号
    :param password:密码
    :return:
    '''
    # 构建一个Session对象,可以保存页面Cookie
    sess = requests.Session()

    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    # 获取登录界面的xsrf
    html = sess.get("https://www.zhihu.com/#signin", headers=headers).text
    # <input type="hidden" name="_xsrf" value="1059e3cdbc0c05dfe480a6f831fc26b6"/>
    regex = '.*name="_xsrf" value="(.*?)"'
    _xsrf_list = re.findall(regex, html)
    _xsrf_list = list(set(_xsrf_list))
    _xsrf = _xsrf_list[0]

    # 判断有无验证码
    # 根据UNIX时间戳，匹配出验证码的URL地址
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)
    # 发送图片的请求，获取图片数据流，
    captcha_data = sess.get(captcha_url, headers=headers).content
    # 获取验证码里的文字，需要手动输入
    text = captcha(captcha_data)

    # 知乎登录
    if re.match("^1\d{10}", account):
        print ("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": _xsrf,
            "phone_num": account,
            "password": password,
            "captcha": text
        }
    else:
        if "@" in account:
            # 判断用户名是否为邮箱
            print("邮箱方式登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": _xsrf,
                "email": account,
                "password": password,
                "captcha": text
        }
    # 发送登录需要的POST数据，获取登录后的Cookie(保存在sess里)
    response = sess.post(post_url, data=post_data, headers=headers)


    # 获取session中cookie 并打印出来
    # cookie = sess.cookies
    # for item in cookie:
    #     print 'name:' + item.name + '  -value:' + item.value

    # 保存session到session文件中
    save_session(sess)

    # 用已有登录状态的Cookie发送请求，获取目标页面源码 https://www.zhihu.com/people/jie-jie-44-85/activities
    response = sess.get("https://www.zhihu.com/people/jie-jie-44-85/activities", headers=headers)
    if response.status_code == 200:
        print '登录成功'
        with open("my.html", "w") as f:
            f.write(response.text.encode("utf-8"))

zhihu_login("1575985731@qq.com", "Qianfeng008")
# zhihu_login("18782902568", "admin123")