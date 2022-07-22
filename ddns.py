import pydnspod
import json
import requests
import time
import datetime
from configparser import ConfigParser
from tenacity import *


cf = ConfigParser()
cf.read('config.ini')                                                  #读取config


token_id = cf.get('config', 'token_id')                                #Token ID
user_token = cf.get('config', 'user_token')                              #Token
domain_id = cf.get('config', 'domain_id')                               #域名ID
record_id = cf.get('config', 'record_id')                               #记录OD
domain = cf.get('config', 'domain')                                  #域名
sub_domain = cf.get('config', 'sub_domain')                              #记录类型
interval = cf.getint('config', 'interval')                              #间隔

@retry()
def get_local_ip():   #获取本机外网ip
    r= requests.get("http://httpbin.org/ip")
    ip=json.loads(r.text)["origin"]
    return ip

@retry()
def get_domain_ip():   #获取解析ip
    json_str = json.dumps(dp.record.info(domain_id,record_id))
    json_str2 = json.loads(json_str)
    return json_str2['value']


dp = pydnspod.connect(token_id, user_token)
while(True):
         print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
         ip = get_local_ip()
         ip2 = get_domain_ip()
         print("     my IP is:    ",ip)
         print("     domain IP is:",ip2)
         if ip==ip2:
            print("     Same, will not change")
            time.sleep(interval)
         else:
            print("     Not same, will change")
            return_=dp.record.modify(domain,record_id,sub_domain,'A',ip)
            if return_ == None:
               print("Failed，retry in 5 mins")
               time.sleep(300)
            else:
                print("Change Successful")
                time.sleep(interval)