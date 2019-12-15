# -*- coding: utf-8 -*-
# @Time   : 2019/4/2011:44
# @Author :lemon_FCC
# @Email  :670992243@qq.com
# @File   :test_login.py
# 类名中间不加下划线

import unittest
from API_01.common.do_HTTPrequ import HTTPrequest
from API_01.common.do_Excel import DoExcel
from API_01.common.do_contants import case_file, case_files
from ddt import ddt, data, unpack


# 跑单个模块用例时，使用
#
# class LoginTest(unittest.TestCase):
#     def setUp(self):
#         # 创建http请求对象session
#         self.http_request = HTTPrequest()
#
#     def test_login(self):
#         doexcel = DoExcel(case_file, 'recharge')
#         cases = doexcel.get_case()
#         for case in cases:
#             resp = self.http_request.request(case.method, case.url, case.data)
#             actual_code = resp.json()['code']
#             try:
#                 self.assertEqual(actual_code, str(case.excepted))
#                 doexcel.write_case(case.case_id+1,resp.text,'PASS')
#             except AssertionError as e:
#                 doexcel.write_case(case.case_id+1,resp.text,'FAIL')
#                 raise e
#
#
#     def tearDown(self):
#         #关闭session
#         self.http_request.close()

# =============================================================================\
# 多个模块用例进行集合，进行测试
# casess=[]
# for i in ['login', 'recharge']:
#     print(type(i))
#     doexcel = DoExcel(case_file, i)
#     cases = doexcel.get_case()
#     casess.extend(cases)
# 优化后的单个用例（充值接口）
@ddt
class LoginTest(unittest.TestCase):
    # 写到类属性中
    doexcel = DoExcel(case_files, 'recharge')
    cases = doexcel.get_case()

    # 转换为类方法，即不用创建对象
    @classmethod  # 用classmethod 装饰类，运行类时启动一次,用一个http请求保存session
    def setUpClass(cls):
        # 创建http请求对象session
        cls.http_request = HTTPrequest()

    @data(*cases)
    def test_case(self, case):
        print(case.title)
        # for case in cases:
        resp = self.http_request.request(case.method, case.url, case.data)
        actual_code = resp.json()['code']
        try:
            self.assertEqual(actual_code, str(case.excepted))
            self.doexcel.write_case(case.case_id + 1, resp.text, 'PASS')
        except AssertionError as e:
            self.doexcel.write_case(case.case_id + 1, resp.text, 'FAIL')
            raise e

    @classmethod  # 修饰为类方法时方法后加Class、
    def tearDownClass(cls):
        # 关闭session
        cls.http_request.close()

        # 注意：在test方法中运行时，会报错（这个方法加载不了类），
        #      因为用了ddt，所以一定要从类开始加载


# git 提交练习
print('git提交练习')
