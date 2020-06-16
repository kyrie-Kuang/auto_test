from django.db import models


# 用户表
class ATUser(models.Model):
    u_username = models.CharField(max_length=16, unique=True)
    u_password = models.CharField(max_length=256)

    class Meta:
        db_table = 'at_user'


# 产品表
class Product(models.Model):
    p_product_name = models.CharField(max_length=64)
    p_product_desc = models.CharField(max_length=200)
    p_product_er = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_product'


# 单个接口用例表
class Apis(models.Model):
    api_pro = models.ForeignKey('Product', on_delete=models.CASCADE)
    api_name = models.CharField(max_length=100)
    api_url = models.CharField(max_length=200)
    api_param_value = models.CharField(max_length=800)
    REQUEST_METHOD = (
        ('0', 'get'),
        ('1', 'post'),
    )
    api_method = models.CharField(choices=REQUEST_METHOD, default='get', max_length=200)
    api_result = models.CharField(max_length=200)
    api_status = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_apis'


# 流程接口用例表
class Apitest(models.Model):
    api_t_pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    api_t_name = models.CharField(max_length=64)
    api_t_desc = models.CharField(max_length=200)
    api_ter = models.CharField(max_length=200)
    api_t_res = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_api_test'


# 流程接口步骤表
class Apistep(models.Model):
    api_test = models.ForeignKey(Apitest, on_delete=models.CASCADE)
    api_name = models.CharField(max_length=100)
    api_step = models.CharField(max_length=200)
    api_url = models.CharField(max_length=800)
    api_param_value = models.CharField(max_length=800)
    REQUEST_METHOD = (
        ('0', 'get'),
        ('1', 'post'),
    )
    api_method = models.CharField(choices=REQUEST_METHOD, default='get', max_length=200)
    api_result = models.CharField(max_length=200)
    api_status = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_api_step'


# Bug管理表
class Bug(models.Model):
    bug_pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    bug_name = models.CharField(max_length=100)
    bug_detail = models.CharField(max_length=500)
    BUG_STATUS = (
        ('激活', '激活'),
        ('已解决', '已解决'),
        ('已关闭', '已关闭'),
    )
    bug_status = models.CharField(choices=BUG_STATUS, default='激活', max_length=200)
    BUG_LEVEL = (
        ('轻微', '轻微'),
        ('一般', '一般'),
        ('严重', '严重'),
    )
    bug_level = models.CharField(choices=BUG_LEVEL, default='严重', max_length=200)
    bug_creat_er = models.CharField(max_length=200)
    bug_assign = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_bug'


# 系统设置表
class Set(models.Model):
    set_name = models.CharField(max_length=200)
    set_value = models.CharField(max_length=600)

    class Meta:
        db_table = 'at_set'


# App用例表
class Apptest(models.Model):
    app_t_pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    app_t_name = models.CharField(max_length=64)
    app_t_desc = models.CharField(max_length=200)
    app_ter = models.CharField(max_length=64)
    app_t_res = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_app_test'


# App 用例步骤表
class Appteststep(models.Model):
    app_test = models.ForeignKey(Apptest, on_delete=models.CASCADE)
    app_step = models.CharField(max_length=200)
    app_find_method = models.CharField(max_length=200)
    app_element = models.CharField(max_length=200)
    app_opt_method = models.CharField(max_length=200)
    app_test_data = models.CharField(max_length=200, null=True)
    app_assert_data = models.CharField(max_length=200)
    app_result = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_app_step'


# Web用例表
class Webtest(models.Model):
    web_t_pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    web_t_name = models.CharField(max_length=64)
    web_t_desc = models.CharField(max_length=200)
    web_ter = models.CharField(max_length=64)
    web_t_res = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_web_test'


# App 用例步骤表
class Webteststep(models.Model):
    web_test = models.ForeignKey(Webtest, on_delete=models.CASCADE)
    web_step = models.CharField(max_length=200)
    web_find_method = models.CharField(max_length=200)
    web_element = models.CharField(max_length=200)
    web_opt_method = models.CharField(max_length=200)
    web_test_data = models.CharField(max_length=200, null=True)
    web_assert_data = models.CharField(max_length=200)
    web_result = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'at_web_step'
