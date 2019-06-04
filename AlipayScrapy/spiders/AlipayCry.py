# 系统库
import datetime
import logging
import requests
import time
from random import choice
import math
import time
import datetime
import random
import json
import traceback
# 项目内部库
import scrapy
import sys, qrtools
from dateutil.relativedelta import relativedelta
# import win32api
# import win32con
import win_unicode_console
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class CheckSecurity(Exception):
    pass

class ErrorSecurity(Exception):
    pass

class LoginSecurity(Exception):
    pass

def log_exception(e):
    print 'str(e):\t\t', str(e)
    print 'repr(e):\t', repr(e)
    print 'e.message:\t', e.message
    print 'traceback.print_exc():'; traceback.print_exc()
    print 'traceback.format_exc():\n%s' % traceback.format_exc()

class XXXClient(object):
    def __init__(self):
        self._url = 'http://localhost:8765'

    def post_info(self, userName, uid):
        pass

    def post_details(self, details):
        if details:
            pass

    # str_type: security, login
    def post_for_qr(self, link_str, str_type):
        pass

    def post_headbeat_status(self, str_status):
        pass

class TimeUtil:
    def __init__(self):
        # 初始化一些日期,时间和时间模板常量
        self.Monday = "周一"
        self.Tuesday = "周二"
        self.Wednesday = "周三"
        self.Thursday = "周四"
        self.Friday = "周五"
        self.Saturday = "周六"
        self.Sunday = "周日"

        self.Morning = "上午"
        self.Afternoon = "下午"
        self.Evening = "晚上"
        self.Midnight = "半夜"

        self.morning_start = "060000"
        self.afternoon_start = "120000"
        self.evening_start = "180000"
        self.evening_end = "235959"
        self.midnight_start = "000000"

        self.time_hms_layout = "%H%M%S"
        self.time_ymd_layout = "%Y%M%D"

    # 获取周几
    def get_week_day(self, date):
        week_day_dict = {
            0: self.Monday,
            1: self.Tuesday,
            2: self.Wednesday,
            3: self.Thursday,
            4: self.Friday,
            5: self.Saturday,
            6: self.Sunday,
        }
        day = date.weekday()
        return week_day_dict[day]

    # 计算日期时间差
    @staticmethod
    def get_time_gap(time_start, time_end):
        start_time_year = int(time_start.split("-")[0])
        start_time_month = int(time_start.split("-")[1])
        start_time_day = int(time_start.split("-")[2])

        end_time_year = int(time_end.split("-")[0])
        end_time_month = int(time_end.split("-")[1])
        end_time_day = int(time_end.split("-")[2])

        return datetime.datetime(end_time_year,
                                 end_time_month,
                                 end_time_day) - datetime.datetime(start_time_year,
                                                                   start_time_month,
                                                                   start_time_day)

    # 计算最大周数
    @staticmethod
    def get_max_week_num(gap):
        if gap >= 0:
            if gap != 0:
                return math.ceil(float(gap / 7))
            else:
                return 0
        else:
            raise ValueError("No time gap or gap is error!")

    # 时间转换为上午,下午,晚上和半夜
    def _divide_time_quantum(self, time_hms, first_time, second_time):
        try:
            if int(time.strftime(self.time_hms_layout, first_time)) <= \
                    int(time.strftime(self.time_hms_layout, time_hms)) < \
                    int(time.strftime(self.time_hms_layout, second_time)):
                return True
            else:
                return False
        except Exception as err:
            print(err.with_traceback(err))

    # 判断时间段
    def get_time_quantum(self, time_hms):
        if self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                     first_time=time.strptime(self.morning_start, self.time_hms_layout),
                                     second_time=time.strptime(self.afternoon_start, self.time_hms_layout)) is True:
            return self.Morning

        elif self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                       first_time=time.strptime(self.afternoon_start, self.time_hms_layout),
                                       second_time=time.strptime(self.evening_start, self.time_hms_layout)) is True:
            return self.Afternoon

        elif self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                       first_time=time.strptime(self.evening_start, self.time_hms_layout),
                                       second_time=time.strptime(self.evening_end, self.time_hms_layout)) is True:
            return self.Evening

        elif self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                       first_time=time.strptime(self.midnight_start, self.time_hms_layout),
                                       second_time=time.strptime(self.morning_start, self.time_hms_layout)) is True:
            return self.Midnight
        else:
            raise ValueError("Variable time_hms is illegal!")

    # 获取当前年月日的前几个月或者后几个月的时间
    @staticmethod
    def get_front_or_after_month(target_date=None, month=0,
                                 day=None, time_format_layout='%Y.%m.%d', timestamp=False):
        """
        :param target_date: str或者是date类型(格式通用,例),如果target_date为空,则默认日期为当天
        :param month: int类型的月份, int < 0 就是前面的月份, int > 0 就是后面的月份
        :param day: int类型的天数,计算后几天的,默认为空,如果不计算后几个月只计算后几天的,month=0即可
        :param time_format_layout: 日期格式化的模板,默认是%Y.%m.%d,输出是2017.11.01
        :param timestamp: 如果timestamp为True则返回时间戳
        :return: 返回target_date和计算完且格式化后的数据
        """
        # 判断目标日期的逻辑
        if target_date is None:
            _date = datetime.datetime.now()
        else:
            # 判断date的类型
            if isinstance(target_date, str):
                _date = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            elif isinstance(target_date, datetime.datetime):
                _date = target_date
            else:
                raise ValueError("Parameter target_date is illegal!")
        _today = _date
        # 判断day的逻辑
        if day is not None:
            if isinstance(day, int):
                _delta = datetime.timedelta(days=int(day))
                _date = _date + _delta
            else:
                raise ValueError("Parameter day is illegal!")
        # 判断month的类型
        if isinstance(month, int):
            _result_date = _date + relativedelta(months=month)
            if timestamp:
                _result_date_ts = int(time.mktime(_result_date.timetuple())) * 1000
                _today_ts = int(time.mktime(_today.timetuple())) * 1000
                return _today_ts, _result_date_ts
            else:
                return _today.strftime(time_format_layout), _result_date.strftime(time_format_layout)
        else:
            raise ValueError("Month is not int,please confirm your variable`s type.")


def slow_input(ele, word):
    for i in word:
        ele.send_keys(i)
        time.sleep(random.uniform(0, 0.5))
# USERAGENT-LIST
ua_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
    "Safari/537.36"]

# 日志基本配置(同时写入到文件和输出到控制台)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger()

# 支付宝爬虫Scrapy版本
class AlipaySpider(scrapy.Spider):
    # Scrapy启动的名字
    name = "AlipaySpider"

    def __init__(self, username, password, option=None, *args):
        # 初始化浏览器
        self._browser = None
        self.processing = True
        # 初始化用户名和密码
        self.username = username
        self.password = password
        self._uid = None
        self._username = None
        self._cache = set()
        self._client = XXXClient()
        # 个人中心和交易记录Url
        self._my_url = 'https://my.alipay.com/portal/i.htm'
        # 登录页面URL(quote_plus的理由是会处理斜杠)
        # self._login_url = 'https://auth.alipay.com/login/index.htm?goto=' + quote_plus(self._my_url)
        self._login_url = 'https://auth.alipay.com/login/index.htm'
        # requests的session对象
        self.session = requests.Session()
        # 将请求头添加到session之中
        self.session.headers = {
            'User-Agent': choice(ua_list),
            'Referer': 'https://consumeprod.alipay.com/record/advanced.htm',
            'Host': 'consumeprod.alipay.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive'}

        # 浏览器初始化配置
        self._load_chrome()
        # cookie存储
        self.cookie = {}
        self.cache = None
        # 交易类别选项(空则默认为1)
        if option is None:
            self.transfer_option = "1"
        else:
            self.transfer_option = str(option)
        # 账单日期筛选
        self.end_date, self.begin_date = TimeUtil.get_front_or_after_month(month=-3)
        # super方法
        super(AlipaySpider, self).__init__(*args)

    # NOT USED set cookies 到 session
    def _set_cookies(self):
        cookie = self.cookie
        self.session.cookies.update(cookie)
        # 输出cookie
        logger.debug(self.session.cookies)
        return True

    # 初始化Chrome
    def _load_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('--user-agent=%s' % choice(ua_list))
        #设置chrome浏览器无界面模式
        options.add_argument('--headless')
        options.add_experimental_option('prefs', {'download.default_directory': '.\\static\\temp_file\\'})
        self._browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)

    # 该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def _is_next_pag_exist(self):
        try:
            self._browser.find_element_by_xpath('//*[@class="page-next page-trigger"]')
            return True
        except Exception as err:
            logger.debug("判断是否存在下一页: " + str(err))
            return False


    def check_infos(self):
        self._username = self.self._browser.find_element_by_xpath('//div[@class="global-account-name"]').get_attribute('title')
        if self._username != self.username:
            return False
        # 获取cookies转换成字典
        cookies = self._browser.get_cookies()
        # cookie字典
        cookies_dict = {}
        for cookie in cookies:
            if 'name' in cookie and 'value' in cookie:
                cookies_dict[cookie['name']] = cookie['value']
                if cookie['name'] == 'CLUB_ALIPAY_COM':
                    self._uid = cookie['value']
        self.cookie = cookies_dict
        if self._uid:
            self._client.post_info(self._username, self._uid)
        return True

    def qr_to_login(self):
        self._browser.get(self._login_url)
        self._client.post_headbeat_status('LOGIN_QR')
        self._browser.find_element_by_xpath('//*[@id="J-loginMethod-tabs"]/li[1]').click()
        self._browser.get_screenshot_as_file(self.username + 'login.png')
        qr = qrtools.QR()
        qr_login_link = ''
        if qr.decode(self.username + 'login.png'):
            qr_login_link = qr.data;
        self._client.post_for_qr('LOGIN', qr_login_link)
        return qr_login_link

    def qr_to_check_secuity(self):
        if 'checkSecurity' in self._browser.current_url:
            self._client.post_headbeat_status('CHECK_SECURITY')
            self._browser.get_screenshot_as_file(self.username + 'checkSecurity.png')
            qr = qrtools.QR()
            qr_check_security_link = ''
            if qr.decode(self.username + 'checkSecurity.png'):
                qr_check_security_link = qr.data
            self._client.post_for_qr('CHECK_SECURITY', qr_check_security_link)
            raise CheckSecurity()
        elif 'error' in self._browser.current_url:
            self._client.post_headbeat_status('ERROR')
            raise ErrorSecurity()
        elif 'login' in self._browser.current_url:
            self._client.post_headbeat_status('LOGIN')
            raise ErrorSecurity()
        else:
            self._client.post_headbeat_status('RUNNING')

    def login(self):
        while True:
            ret = self.try_login_password()
            if ret = 1:
                self.qr_to_login()
                continue
            elif ret = 2:
                self.qr_to_check_secuity()
                continue
            else:
                pass
            if not passself.check_infos():
                continue
            else:
                break

    def try_login_password(self):
        # self._browser.maximize_window()
        self._browser.get(self._login_url)
        # self._browser.implicitly_wait(3)
        # 点击密码登录的选项卡
        self._browser.find_element_by_xpath('//*[@id="J-loginMethod-tabs"]/li[2]').click()
        # 用户名输入框
        username = self._browser.find_element_by_id('J-input-user')
        username.clear()
        logger.info('正在输入账号.....')
        slow_input(username, self.username)
        time.sleep(random.uniform(0.4, 0.8))
        # 密码输入框
        password = self._browser.find_element_by_xpath('//*[@id="password_container"]/input')
        password.clear()
        logger.info('正在输入密码....')
        slow_input(password, self.password)
        # 登录按钮
        time.sleep(random.uniform(0.3, 0.5))
        self._browser.find_element_by_id('J-login-btn').click()
        # 输出当前链接
        logger.info("当前页面链接: " + str(self._browser.current_url))
        if self._browser.current_url == self._login_url:
            return 1  # 需要进行二维码登陆
        if "checkSecurity" in self._browser.current_url:
            return 2 # 需要进行交互验证
        else:
            return 3 # 登陆成功

    def get_detail_page(self, week=False):
        # 下拉框a标签点击事件触发
        if week:
            self._browser.find_element_by_xpath('//*[@id="J-datetime-select"]/a[1]').click()
        else:
            self._browser.find_element_by_xpath('//*[@id="J-datetime-select"]/a[0]').click()
        # 选择下拉框的选项
        self._browser.find_element_by_xpath('//ul[@class="ui-select-content"]/li[@data-value="sevenDays"]'). click()
        # 智能等待 --- 2
        time.sleep(random.uniform(0.5, 0.9))
        # 选择交易分类
        self._browser.find_element_by_xpath('//div[@id="J-category-select"]/a[1]').click()
        # 选择交易分类项
        self._browser.find_element_by_xpath('//ul[@class="ui-select-content"]/li[@data-value="TRANSFER"]').click()
        # 智能等待 --- 3
        time.sleep(random.uniform(1, 2))
        # TODO self._browser.find_element_by_xpath('//*[@name="fundFlow"]').click()
        # 即时到账
        self._browser.find_element_by_xpath('//*[@id="instant"]').click()
        # 按钮(交易记录点击搜索)
        self._browser.find_element_by_id("J-set-query-form").click()
        logger.info("跳转到自定义时间页面....")
        logger.info(self._browser.current_url)
        self.qr_to_check_secuity()

    # 解析账单页面
    def parse_all_detail(self):
        self.qr_to_check_secuity()
        bill_sel = scrapy.Selector(text=self._browser.page_source)
        # 选取的父标签
        trs = bill_sel.xpath("//tbody//tr")
        # 判断是否存在下一页的标签
        is_next_page = self._is_next_pag_exist()
        # 开始获取第一页的数据
        result = []
        for tr in trs:
            bill_info = dict(flowType='ALIPAY_TRANSFER',
                             outerAccountName=self.username,
                             outerType='OUT_ALIPAY_PERSONAL')
            # 交易时间(年月日)
            transfer_ymd = tr.xpath('string(td[@class="time"]/p[1])').extract()[0].strip()
            # 交易时间(时分秒)
            transfer_hms = tr.xpath('string(td[@class="time"]/p[2])').extract()[0].strip().replace(":", "") + "00"
            bill_info['flowDatetime'] =transfer_ymd + " " + transfer_hms
            # memo标签(交易备注)
            transfer_memo = None
            try:
                transfer_memo = tr.xpath('string(td[@class="memo"]/'
                                                      'div[@class="fn-hide content-memo"]/'
                                                      'div[@class="fn-clear"]/p[@class="memo-info"])'
                                                      ).extract()[0].strip()
            except IndexError:
                logger.debug("Transfer memo exception: transfer memo is empty!")
                transfer_memo = ""
            bill_info['flowMemo'] = transfer_memo
            # 交易名称
            transfer_name = None
            try:
                transfer_name = tr.xpath('string(td[@class="name"]/p/a)').extract()[0].strip()
            except IndexError:
                try:
                    transfer_name = tr.xpath('string(td[@class="name"]/p/text())').extract()[0].strip()
                except IndexError:
                    logger.debug("Transfer name exception 2: Transfer name is empty!")
                    transfer_name = ""
            bill_info['flowName'] = transfer_memo
            # 交易订单号(商户订单号和交易号)
            code = tr.xpath('string(td[@class="tradeNo ft-gray"]/p)').extract()[0]
            if "|" not in code:
                bill_info['flowId'] = code.split(":")[-1]
                if bill_info['flowId'] in self._cache:
                    is_next_page = False
                    break;
                bill_info['flowOrderId'] = ""
            else:
                code_list = code.split(" | ")
                bill_info['flowId'] = ""
                bill_info['flowOrderId'] = code_list[0].split(":")[-1] + "-" + code_list[-1].split(":")[-1]

            # 对方(转账的标签有不同...奇葩的设计)
            if bill_info['flowMemo'] == "":
                bill_info['flowOtherName'] = tr.xpath('string(td[@class="other"]/p[@class="name"]/span)').extract()[0].strip()
                if bill_info['flowOtherName'] == "":
                    bill_info['flowOtherName'] = tr.xpath('string(td[@class="other"]/p[@class="name"])').extract()[0].strip()
            else:
                bill_info['flowOtherName'] = tr.xpath('string(td[@class="other"]/p[@class="name"]/span)').extract()[0].strip()
                if bill_info['flowOtherName'] == "":
                    bill_info['flowOtherName'] = tr.xpath('string(td[@class="other"]/p)').extract()[0].strip()
            # 输出测试
            result += [bill_info]

        logger.info("是否存在下一页: " + str(is_next_page))
        if is_next_page:
            # 智能等待 --- 3
            time.sleep(random.uniform(0.3, 0.6))
            self._browser.execute_script('window.scrollTo(0,10000000)')
            time.sleep(random.uniform(0.5, 0.9))
            self._browser.find_element_by_xpath('//*[@class="page-next page-trigger"]').click()
            result += self.parse()
        return result


    def process(self):
        login()
        self._browser.find_element_by_xpath('//ul[@class="global-nav"]/li[@class="global-nav-item "]/a').click()
        while self.processing:
            try:
                get_detail_page(week)
                all_detail = self.parse_all_detail()
                self._client.post_details(all_detail)
                for detail in all_detail:
                    self._cache.add(detail['flowId'])
                time.sleep(random.uniform(10, 30))
            except Exception as e:
                log_exception(e)
                if e isinstance CheckSecurity:
                    while self.processing:
                        self._browser.
                        time.sleep(random.uniform(10, 30))
                else:
                    raise e

    def do_process(self):
        while self.processing:
            try:
                self.process()
            except Exception as e:
                log_exception(e)


        self._browser.quit()


            # post;



if __name__ == '__main__':
    asp = AlipaySpider("abaobo199@gmail.com", "sunjinbao199")

    result = []
    try:
        a = asp.start_requests()
    except Exception as e:
        pass
    if asp._browser:
        asp._browser.quit()
