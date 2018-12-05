# -*- coding=utf-8 -*-
from datetime import datetime
from tools.push_tools import PushTool
import requests
import sys
from configparser import ConfigParser
from urllib import parse
import traceback

success_count = 0
failure_count = 0
start_time = datetime.now()
cookie = PushTool.get_cookies()
config = ConfigParser()
config.read('config.ini', 'utf-8')
target = config.get('bd_push', 'target')


class BDManual:

    @staticmethod
    def bd_manual(num):
        global success_count
        global failure_count
        global start_time
        global target

        while True:
            url = PushTool.rand_all(target)
            data = 'url=%s' % parse.quote_plus(url)
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': str(len(data)),
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'BIDUPSID=358AB784CA9B61AE0BB262CA5B63C31F; PSTM=1543830159; BAIDUID=10F2B0EDBCCA246B1096F100C2D54A10:FG=1; H_PS_PSSID=1433_21118_26350_27508; Hm_lvt_6f6d5bc386878a651cb8c9e1b4a3379a=1543888479; lastIdentity=PassUserIdentity; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02939879255; delPer=0; PSINO=7; locale=zh; __cas__rn__=293987925; BDUSS=nU1fmdmVU92SThBRU8tNDQ0T3RxcFd3Zjhoa2g1cVdwZGZXYUxNeTZycHcyQzVjQVFBQUFBJCQAAAAAAAAAAAEAAABmnim80rvJ-tK7ysDWwtS2NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBLB1xwSwdcQ; SITEMAPSESSID=iope24msj5s1rfcu9qlpmdv5l4; Hm_lpvt_6f6d5bc386878a651cb8c9e1b4a3379a=1543981941',
                'Host': 'ziyuan.baidu.com',
                'Origin': 'https://ziyuan.baidu.com',
                'Referer': 'https://ziyuan.baidu.com/linksubmit/url',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'X-Request-By': 'baidu.ajax',
                'X-Requested-With': 'XMLHttpRequest',
            }
            conn = requests.Session()
            conn.headers = headers
            # print(headers)
            # 将cookiesJar赋值给会话
            cookiesJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
            conn.cookies = cookiesJar
            code = 404
            try:
                res = conn.post('https://ziyuan.baidu.com/linksubmit/urlsubmit', headers=headers, data=data, timeout=3.0)
                code = res.status_code
                if code == 200:
                    if '{"over":0,"status":0}' in res.text:
                        success_count += 1
                    else:
                        failure_count += 1
                else:
                    failure_count += 1
            except:
                traceback.print_exc()
                failure_count += 1
            this_time = datetime.now()
            spend = this_time - start_time
            if int(spend.seconds) == 0:
                speed_sec = success_count / 1
            else:
                speed_sec = success_count / int(spend.seconds)
            speed_day = float('%.2f' % ((speed_sec * 60 * 60 * 24) / 10000000))
            percent = success_count / (failure_count + success_count) * 100
            sys.stdout.write(' ' * 100 + '\r')
            sys.stdout.flush()
            print(url)
            sys.stdout.write(
                '%s 成功%s 预计(day/千万):%s M 成功率:%.2f%% 状态码:%s\r' % (
                datetime.now(), success_count, speed_day, percent, code))
            sys.stdout.flush()