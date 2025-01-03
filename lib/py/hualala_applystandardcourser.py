import datetime
import numbers
import random
from datetime import date

import xlwt
from openpyxl import Workbook
import openpyxl
# from spire.xls import *
import pandas as pd
import numpy as np
from openpyxl.reader.excel import load_workbook
from openpyxl.styles.numbers import NumberFormat
from openpyxl.workbook import Workbook

from bin.runMySQL import mysqlMain
from conf.readconfig import getConfig
from lib.py.hualala_update_userinfo import UpdateUserInfoRun
from lib.py.order_V2_script import *
import requests
import xlsxwriter
import json
import pandas as pd
import os, time

# import oss2
# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client

from conf.readconfig import *


class ApplyStandardCourserRun():

    def getFileStream_Order(self, phone, sku_id, marketing_id):
        file_name = "example.xlsx"
        # 获取当前日期和时间
        now = datetime.date.today()
        now1 = datetime.datetime.now()
        # 将日期和时间转换为字符串格式
        date_str = now1.strftime("%y%m%d%H%M%S")
        out_orderNumber = date_str
        # 创建一个新的Excel文件并添加一个工作表
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        # 写入数据行
        data = [["填写须知", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["填写须知", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["填写须知", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["*第三方订单号", "*用户姓名", "*手机区号", "*手机号", "*画啦啦学员ID", "学员注册渠道代号", "*套餐ID",
                 "*活动配置ID", "*支付方式",
                 "收款账号", "平台优惠金额", "*支付日期", "是否需要地址", "收件人",
                 "国家", "联系电话", "省", "市", "区", "详细地址", "用户备注", "退费信息留言"],
                [int(out_orderNumber), "测试学员", 86, int(phone), "", "", int(sku_id), int(marketing_id), "抖音小店", "", "", now,
                     0, "", "", "", "", "", "", "", "", ""]
        ]
        for row_num, data_row in enumerate(data, start=0):
            for col_num, value in enumerate(data_row):
                worksheet.write(row_num, col_num, value)
        #将支付时间修改为日期格式
        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
        worksheet.write_datetime(4, 11, now, date_format)
        # 保存工作簿
        workbook.close()
        return file_name

    def getLiuyiToken(self, choose_url):
        auth_url = getConfig("liuyi-url", choose_url)
        account = getConfig("liuyi-login", choose_url + "_phone")

        url_path = "/oa-user-center/sso/login?account=" + account + "&password=e10adc3949ba59abbe56e057f20f883e&smsCode=1234"
        headers = {
            'content-type': 'application/json'
        }
        response = requests.request("POST", auth_url + url_path, headers=headers)
        re = json.loads(response.text)
        print(re)
        try:
            return re['data']['accessToken']
        except KeyError as e:
            # 异常时，执行该块
            return False, e
            pass

    def importCreateNew(self,mobile, file_path, Authorization, choose_url):
        gw_url = getConfig("liuyi-url", choose_url)
        url_path = "/manager-api/o/standard/applySignUp/importCreateNew"
        headers = {
            'authorization': Authorization,
            'Accept': 'application/json, text/plain, */*',
            'priority': 'u=1, i'
        }
        files = {
            'file': open(file_path, 'rb')
        }
        print(files)
        response = requests.request("POST", gw_url + url_path, headers=headers, files=files)
        print("导入订单" + response.text)
        # re = json.loads(response.text)
        # if int(re['code']) in order_error_code: return int(re['code']), re['message']
        time.sleep(2)
        res=self.user_order_status(mobile,choose_url)
        return res
    def user_order_status(self,mobile,choose_url):

        if choose_url == "test":
            mysql_conn = mysqlMain('MySQL-Liuyi-test')
        else:
            mysql_conn = mysqlMain('MySQL-Liuyi-preprod')

        sql_user = "SELECT UserId FROM i61.userinfo  WHERE Account ='%s'" % mobile +""
        try:
            if mobile is not None:
                userid = mysql_conn.fetchone(sql_user)
                if userid is None:
                    # print(userid['UserId'])
                    return False, "导入失败，该手机号没有进线学员"
                else:
                    user=userid['UserId']
                    print(userid['UserId'])
                    order_import_sql = "SELECT * FROM `i61-hll-manager`.`import_user_standard_course_record`  WHERE `user_id` ='%s'" % user+"ORDER BY id DESC"
                    order = mysql_conn.fetchall(order_import_sql)
                    print(order)
                    order_id=order[0]['id']
                    order_user_id=order[0]['user_id']
                    order_state=order[0]['state']
                    order_fail_reason=order[0]['fail_reason']
                    if order_state ==3 :
                        return False,order_user_id,order_fail_reason
                    else:
                        return True,order_id,order_user_id,"导入成功"
                    print(order_state,order_fail_reason)
                    str1 = "手机号：" + mobile
                    str2 = "用户id：" + str(userid['UserId'])
                    return True, "test"
            else:
                return False,"导入失败"
        except Exception as e:
            print("数据修改失败：", e)
            return False
        finally:
            del mysql_conn

    def order_audit(self,Authorization,import_id,choose_url):
        gw_url = getConfig("liuyi-url", choose_url)
        url_path = "/manager-api/o/standard/applySignUp/batchAudit"
        headers = {
            'content-type': 'application/json',
            'authorization': Authorization
        }
        datas = json.dumps({
              "ids": [import_id],
              "state": 3
            })
        print(datas)
        response = requests.request("POST", gw_url + url_path, headers=headers, data=datas)
        print("审批通过" + response.text)
        re = json.loads(response.text)
        if re['code'] != 0:
            print("审批失败",re)
            return False,re
        else:
            return True,re
        # re = json.loads(response.text)
        # if int(re['code']) in order_error_code: return int(re['code']), re['message']
    def select_applystandercourse(self,choose_url,choose_sku_id,choose_tools):
        gw_url = getConfig("liuyi-gw-mg-url", choose_url)
        # print(gw_url)
        Authorization = self.getLiuyiToken(choose_url)
        url_path = '/hll-standard-course/o/standard/course/get/detail/info?skuIds='+str(choose_sku_id)+'&isOriginalPrice=0&isTwins=0&hasTools='+str(choose_tools)+'&tagName=%E5%85%A8%E9%87%8F&teacherId='
        headers = {
            # 'content-type': 'application/json',
            'authorization': Authorization
        }
        response = requests.request("POST", gw_url + url_path, headers=headers)
        print("查询结果：" + response.text)
        re = json.loads(response.text)
        return re

    def run(self, choose_url, phone, sku_id, marketing_id):
        # if choose_url == 'pro' : channel_id = 467263
        Authorization = self.getLiuyiToken(choose_url)
        if Authorization is False: return False, "登录失败"
        file_path = self.getFileStream_Order(phone, sku_id, marketing_id)
        if file_path is False: return False, "excel文件创建失败"
        UpdateUserInfoRun().UpdateUserInfo(phone,choose_url)
        # if choose_url == 'pro':
        #     if type(phone) == list:
        #         for mobile in phone:
        #             result = self.chenckPhoneIsTest(mobile, Authorization, hourId)
        #             if result != 0:
        #                 return False, result
        try:
            res = self.importCreateNew(phone,file_path, Authorization, choose_url)
            os.remove(file_path)
            print(res)
            if res[0] == True:
                time.sleep(3)
                self.order_audit(Authorization,res[1],choose_url)
                print("分割线")
                print(res)
                result = "学员id："+str(res[2])+",学员生成首报订单成功！"
                return result
            else:
                return False,res
            # 主代码块
            # return True, "Success"
            pass
        except KeyError as e:
            # 异常时，执行该块
            return False, "False"
            pass
        except IndexError as e:
            # 异常时，执行该块
            return False, "False"
            pass
        finally:
            # 无论异常与否，最终执行该块
            pass

if __name__ == '__main__':
    print("执行开始。。。。")
    choose_url = "test"  # test, pro
    # Authorization = ''
    phone = '14055502412'
    sku_id = 201
    marketing_id = 603

    # sku_id = 313
    # marketing_id = 295
    Authorization = "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoicElsYnJxeGh4dmlqbWFCamR5b3F5ZzV0YW1kRk9Qdzg2azRCQ0FGbzhUdmNWMERJcFpXaFlyMnk5ZDk3RkR3bjRhbDAxRUxmUlNqVUVlbm56QzV6clR5T2xRT0UvUUhQdGhmOFBCdEJUV0VBN2h4Yzh0ZDRyT1k5MzFXWGpRL1JmTmdYclVDeERnYjUzeEVCcFI1ejFoOXFHWTdjZGNCVG53aE1xWVZRREtPVlV3OFF1Ry9GYWZtMWZwaXBWLzdaNG5xL3h4ZXRlRzFJd2FSdHRqZEJXbVNia1pHUVFEbDdraCt2MEJtS005eDgyd2FtaFlpNSt3bUVtSGlGZVFNWjMwd2NMY2U0Y01iWTI3WTB5MWxsM3dBWFovVEEwNndjVVdDNzFqZlhHb0p1aWRjS2xBR0FmVS9wYnphbVlDS0YiLCJleHAiOjE3Mzc1MzE1Mjd9.emZdVPH3BbQgdIf7m4zqnxXOqTltLz8TlfCzaZjCcaA"
    user_id=1409329
    # re = ApplyStandardCourserRun().getFileStream_V3_yuwen_batch(user_id,Authorization)

    file_path = "example.xlsx"
    # re = ApplyStandardCourserRun().getFileStream_Order(phone, sku_id, marketing_id)
    re = ApplyStandardCourserRun().getLiuyiToken(choose_url)
    # re = ApplyStandardCourserRun().importCreateNew(mobile,file_path,Authorization,choose_url)
    re = ApplyStandardCourserRun().run(choose_url,phone, sku_id, marketing_id)
    # re = ApplyStandardCourserRun().user_order_status(phone, choose_url)
    # re=ApplyStandardCourserRun().select_applystandercourse(choose_url,sku_id,str(0))
    #

    print("执行结束88,", re)
