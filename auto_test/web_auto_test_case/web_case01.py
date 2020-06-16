# conding=utf-8

import unittest
import time
import pymysql
from selenium import webdriver
import HTMLTestRunner


class Search(unittest.TestCase):
    # 搜索： webUI自动化测试

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.baidu.com")

    def test_readSQL_case(self):
        sql = "SELECT id,web_find_method,web_element,web_opt_method,web_test_data,web_assert_data,web_result FROM at_web_step where at_web_step.web_test_id=1;"

        coon = pymysql.connect(
            user='root',
            passwd='123456',
            port=3306,
            host='127.0.0.1',
            db='autotest_',
            charset='utf8'
        )
        cursor = coon.cursor()
        a = cursor.execute(sql)
        b = cursor.fetchmany(a)
        for i in b:
            case_list = []
            case_list.append(i)
            web_test_case(case_list, self)
        coon.commit()
        cursor.close()
        coon.close()

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()


def web_test_case(case_list, self):
    for case in case_list:
        try:
            case_id = case[0]
            find_method = case[1]
            element = case[2]
            opt_method = case[3]
            test_data = case[4]
        except Exception as e:
            return 'error' % e
        
        print(case)
        time.sleep(1)

        if opt_method == "sendkeys" and find_method == "find_element_by_id":
            self.driver.find_element_by_id(element).send_keys(test_data)
            print(element)
        elif opt_method == "click" and find_method == "find_element_by_id":
            self.driver.find_element_by_id(element).click()
            print(element)


if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d-%H_%M_%S")

    all_case_list = "E:\\auto_test\\web_auto_test_case"

    test_unit = unittest.TestSuite()
    test_unit.addTest(Search("test_readSQL_case"))

    file_name = "E:\\auto_test\\web_auto_test_case\\report\\" + now +"_web_reprot.html" 

    fn = open(file_name, 'wb')

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fn,
        title=u'web自动化测试报告',
        description=u'搜索测试用例'
    )
    runner.run(test_unit)
