import random
from datetime import date

import numpy as np

from bin.runMySQL import mysqlMain
from conf.readconfig import getConfig
from lib.py.order_V2_script import *
import requests
import json
import pandas as pd
import os, time

# import oss2
# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client

from conf.readconfig import *

class UserConsumeHoursRun():
    #获取签名sign接口
    def getLiuyiToken(self, choose_url):
        auth_url = getConfig("liuyi-url", choose_url)
        account = getConfig("liuyi-login", choose_url + "_phone")
        # print(auth_url)

        url_path = "/oa-user-center/sso/login?account=" + account + "&password=e10adc3949ba59abbe56e057f20f883e&smsCode=1234"
        # payload = json.dumps({
        #     "username": getConfig("crm-login", choose_url + "_phone"),
        #     "password": getConfig("crm-login", choose_url + "_pwd"),
        #     "__fields": "token,uid"
        # })
        headers = {
            'content-type': 'application/json'
        }
        response = requests.request("POST", auth_url + url_path,  headers=headers)
        re = json.loads(response.text)
        print(re)
        # print(re['data']['accessToken'])
        # print(re['data']['token'])
        try:
            return re['data']['accessToken']
        except KeyError as e:
            # 异常时，执行该块
            return False, e
            pass

    # 到课消课记录，查询待消课的记录
    def get_takeAndConsume_list(self,choose_url,Authorization,userid,course_type):

        cms_url = getConfig("liuyi-url", choose_url)
        url = '/manager-api/o/course/takeAndConsume/getList'
        headers = {
            'content-type': 'application/json',
            "authorization": Authorization
        }
        params_data = {
                        "page":1,
                        "size":30,
                        "startDate": "2020-01-01",
                        "endDate": "2025-12-31",
                        "courseTimeScheduleId":0,
                        "workGroupId":0,
                        "teacherId":0,
                        "consumeStatus":0,
                        "courseType":course_type,
                        "userName":userid,
                        "groupName":"",
                        "belongArea":"",
                        "userId":"",
                        "teacherName":""
                       }
        res = requests.get(url=cms_url+url, params=params_data,headers=headers)

        if json.loads(res.text)["data"]["count"] == 0:
            # print(userid['UserId'])
            print("消课失败")
            return "消课失败，该学员没有可消课的上课记录"

        else:
            # res = requests.request("POST", cms_url + url, params=params_data, headers=headers)
            print("输出"+res.text)
            re_data = json.loads(res.text)["data"]["data"]
            # print("data:"+re_data)
            for i in range(len(re_data)):
                id = json.loads(res.text)["data"]["data"][i]["id"]
                print(id)
                self.commit_manual_consume(id,choose_url,Authorization)
                i += 1
            self.query_playback_record(choose_url, Authorization, userid)
            return "消课成功!"



    # 到课消课记录，操作手动消课
    def commit_manual_consume(self,id,choose_url,Authorization):

        cms_url = getConfig("liuyi-url", choose_url)
        url = cms_url + '/manager-api/o/course/takeAndConsume/commitManualConsume'
        headers = {
            "authorization": Authorization,
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "accept":"application/json, text/plain, */*"
        }
        data = {
                "id":id,
                "url":"https%3A%2F%2Fhualala-common.oss-cn-shenzhen.aliyuncs.com%2Ftest%2Fcms%2F6550cf8ef4edcc0001ac66df.png",
                "reason": "9512345678977777777",
                "type": 2
        }
        res = requests.session().post(url=url, data=data,headers=headers)
        print(json.loads(res.text))


    # 消课审核-查询接口
    def query_playback_record(self,choose_url,Authorization,userid):
        cms_url = getConfig("liuyi-url", choose_url)
        url = cms_url + '/manager-api/o/apply/playbackRecord/query.json'
        headers = {
            "authorization": Authorization
        }
        data = {
                "groupId": 0,
                "teacherId": 0,
                "user": userid,
                "page": 1,
                "size": 20,
                "state": 1
        }
        res = requests.session().post(url=url, data=data,headers=headers)
        print(json.loads(res.text))
        re_data = json.loads(res.text)["data"]["list"]

        for i in range(len(re_data)):
            id = json.loads(res.text)["data"]["list"][i]["id"]
            self.agree_playback_record(id,choose_url,Authorization)
            i += 1



    # 同意消课审核
    def agree_playback_record(self,id,choose_url,Authorization):
        cms_url = getConfig("liuyi-url", choose_url)
        url = cms_url + '/manager-api/o/apply/playbackRecord/updateState.json'
        headers = {
            "authorization": Authorization
        }
        data = {
                "id": id,
                "state": 2,
                "reason": "",
                "type": 2,

        }
        res = requests.session().post(url=url, data=data,headers=headers)
        print(json.loads(res.text))

    # 操作取消消课和同意消课审核
    # def operate_student_cancel_classes(self,userid):
    #     self.get_takeAndConsume_list(userid)
    #     self.query_playback_record(userid)

    def run(self,choose_url,user_id,course_type):
        Authorization = self.getLiuyiToken(choose_url)
        res = self.get_takeAndConsume_list(choose_url,Authorization,user_id,course_type)
        return res

if __name__ == '__main__':
    print("执行开始。。。。")
    env_select = "pre" # test, pro
    # Authorization = ''
    user_id='1395617'
    orderNum = '132456'
    course_type=10
    # re = UserConsumeHoursRun(env_select).operate_student_cancel_classes(orderNum)
    # re=UserConsumeHoursRun().getLiuyiToken(env_select)
    re = UserConsumeHoursRun().run(env_select,user_id,course_type)
    print("执行结束88,",user_id,re)


