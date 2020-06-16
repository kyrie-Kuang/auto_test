from django.urls import path

from api import views

urlpatterns = [
    # 登陆页面
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # 产品页面
    path('product_manage/', views.product_manage, name='product_manage'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_delete/', views.product_delete, name='product_delete'),
    path('update_product/', views.update_product, name='update_product'),

    # 接口页面
    path('apis_manage/', views.apis_manage, name='apis_manage'),
    path('add_apis/', views.add_apis, name='add_apis'),
    path('apis_update/', views.apis_update, name='apis_update'),
    path('apis_delete/', views.apis_delete, name='apis_delete'),

    # 流程页面
    path('api_test_manage/', views.api_test_manage, name='api_test_manage'),
    path('add_api_test/', views.add_api_test, name='add_api_test'),
    path('api_delete/', views.api_delete, name='api_delete'),
    path('api_update/', views.api_update, name='api_update'),

    # 流程接口步骤页面
    path('api_step_manage/', views.api_step_manage, name='api_step_manage'),
    path('add_api_step/', views.add_api_step, name='add_api_step'),
    path('api_step_delete/', views.api_step_delete, name='api_step_delete'),
    path('api_step_update/', views.api_step_update, name='api_step_update'),

    # Bug页面
    path('bug_manage/', views.bug_manage, name='bug_manage'),
    path('add_bug/', views.add_bug, name='add_bug'),
    path('bug_delete/', views.bug_delete, name='bug_delete'),
    path('bug_update/', views.bug_update, name='bug_update'),

    # 系统设置页面
    path('set_manage/', views.set_manage, name='set_manage'),
    path('add_set/', views.add_set, name='add_set'),
    path('set_user_manage/', views.set_user_manage, name='set_user_manage'),

    # app用例页面
    path('app_test_manage/', views.app_test_manage, name='app_test_manage'),
    path('add_app_test/', views.add_app_test, name='add_app_test'),
    path('app_delete/', views.app_delete, name='app_delete'),
    path('app_update/', views.app_update, name='app_update'),

    # app用例步骤页面
    path('app_step_manage/', views.app_step_manage, name='app_step_manage'),
    path('add_app_step/', views.add_app_step, name='add_app_step'),
    path('app_step_delete/', views.app_step_delete, name='app_step_delete'),
    path('app_step_update/', views.app_step_update, name='app_step_update'),

    # web用例页面
    path('web_test_manage/', views.web_test_manage, name='web_test_manage'),
    path('add_web_test/', views.add_web_test, name='add_web_test'),
    path('web_delete/', views.web_delete, name='web_delete'),
    path('web_update/', views.web_update, name='web_update'),

    # web用例步骤页面
    path('web_step_manage/', views.web_step_manage, name='web_step_manage'),
    path('add_web_step/', views.add_web_step, name='add_web_step'),
    path('web_step_delete/', views.web_step_delete, name='web_step_delete'),
    path('web_step_update/', views.web_step_update, name='web_step_update'),

    # 测试报告页面
    path('apis_report/', views.apis_report, name='apis_report'),
    path('api_test_report/', views.api_test_report, name='api_test_report'),
    path('web_report/', views.web_report, name='web_report'),
    path('app_report/', views.app_report, name='app_report'),

    # celery定时任务页面
    path('celery_manage/', views.celery_manage, name='celery_manage'),
    path('celery_delete/', views.celery_delete, name='celery_delete'),

    # 搜索功能页面
    path('pro_search/', views.pro_search, name='pro_search'),
    path('apis_search/', views.apis_search, name='apis_search'),
    path('api_test_search/', views.api_test_search, name='api_test_search'),
    path('web_search/', views.web_search, name='web_search'),
    path('app_search/', views.app_search, name='app_search'),
    path('bug_search/', views.bug_search, name='bug_search'),

    # Jenkins持续集成、Locust性能测试页面
    path('jenkins_page/', views.jenkins_page, name='jenkins_page'),
    path('locust_page/', views.locust_page, name='locust_page'),
    path('celery_page/', views.celery_page, name='celery_page'),

    # Celery test
    path('do/', views.do, name='do'),
]
