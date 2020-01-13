# auto_test
通过Python+Django+Bootstrap编写的自动化测试平台。

可在平台上进行，接口，app，web自动化测试用例编写，并执行对应用例py文件，生成html测试报告，含提BUG功能；
可在平台进行Celery异步任务，定时任务执行；
可在平台进行Jenkins持续集成；
可在平台进行Locust性能测试；

自动化测试平台使用步骤：（例：web自动化测试） 
1，添加相关产品 
2，添加web自动化测试用例 
3，添加web自动化测试用例步骤 
4，运行web自动化测试case py文件（可在平台通过Celery执行定时任务，或通过Jenkins持续集成），自动生成html测试报告
5，测试报告页面查看报告文件存放路径
6，打开html报告文件查看测试用例执行情况
（可进行Celery异步任务，定时任务执行）
（可集成到Jenkins持续集成）
（可进行Locust性能测试）


首页
![home](https://github.com/kyrie-Kuang/auto_test/blob/master/home_1.png)
产品列表
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/product.png)
web自动化用例列表
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/web_test.png)

web自动化用例步骤列表
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/web_step.png)

web自动化用例py执行文件
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/web_case.png)

Celery定时任务列表
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/celery_manage.png)

admin后台编辑Celery
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/celery_update.png)

web自动化用例报告路径
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/web_report.png)

web自动化用例html报告
![product](https://github.com/kyrie-Kuang/auto_test/blob/master/web_html.png)


接口用例列表
![apitest](https://github.com/kyrie-Kuang/auto_test/blob/master/api_test.png)

添加接口用例
![add_apitest](https://github.com/kyrie-Kuang/auto_test/blob/master/add_apitest.png)

Bug列表
![bug_l](https://github.com/kyrie-Kuang/auto_test/blob/master/bug_l.png)


