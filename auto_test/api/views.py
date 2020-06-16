from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from api.models import ATUser, Product, Apis, Apitest, Apistep, Bug, Set, Apptest, Appteststep, Webtest, Webteststep
import os
from djcelery.models import PeriodicTask, CrontabSchedule, IntervalSchedule

from api.tasks import ApiTask


def index(request):
    return HttpResponse('index')


# 登陆
def login(request):
    if request.method == "GET":
        data = {
            'title': '登陆',
        }
        return render(request, 'login.html', context=data)
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = ATUser.objects.filter(u_username=username)

        if users.exists():
            user = users.first()

            if check_password(password, user.u_password):
                request.session['user_id'] = user.id

                return redirect(reverse("at:home"))
            else:
                return redirect(reverse("at:login"))
        return redirect(reverse("at:login"))


# 注册
def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册'
        }
        return render(request, 'register.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = ATUser.objects.filter(u_username=username)

        if username == "" or users.exists():
            return redirect(reverse('at:register'))

        else:
            password = make_password(password)

            user = ATUser()
            user.u_username = username
            user.u_password = password
            user.save()

            return redirect(reverse('at:login'))
    return redirect(reverse('at:register'))


# 首页
def home(request):
    user_id = request.session.get('user_id')

    data = {
        'title': '首页',
        'username': 'username'
    }
    if user_id:
        user = ATUser.objects.get(id=user_id)
        data['username'] = user.u_username
        return render(request, 'home.html', context=data)


# 登出
def logout(request):
    request.session.flush()
    return redirect(reverse('at:login'))


# 产品中心
def product_manage(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '产品中心',
        'products': page_object,
    }

    return render(request, 'product_manage.html', context=data)


# 添加产品
def add_product(request):
    if request.method == 'GET':
        data = {
            'title': '添加产品'
        }

        return render(request, 'add_product.html', context=data)

    elif request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_desc = request.POST.get('product_desc')
        product_er = request.POST.get('product_er')

        products = Product.objects.filter(p_product_name=product_name)

        if product_name == "" or products.exists():
            return redirect(reverse('at:add_product'))

        else:
            product = Product()

            product.p_product_name = product_name
            product.p_product_desc = product_desc
            product.p_product_er = product_er
            product.save()

            return redirect(reverse('at:product_manage'))
    return redirect(reverse('at:add_product'))


# 编辑产品
def update_product(request):
    p_id = request.GET.get('product.id')
    product = Product.objects.filter(id=p_id).first()
    # p = Product.objects.get(id=p_id)
    # products = Product.objects.all()
    data = {
        'title': '修改产品',
        'product': product,
        # 'p': p,
    }

    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_desc = request.POST.get('product_desc')
        product_er = request.POST.get('product_er')

        if product_name == "":
            return render(request, 'update_product.html', context=data)

        Product.objects.filter(id=p_id).update(
            p_product_name=product_name,
            p_product_desc=product_desc,
            p_product_er=product_er
        )

        return redirect(reverse('at:product_manage'))
    return render(request, 'update_product.html', context=data)


# 删除产品
def product_delete(request):
    # pro_id = request.GET.get('product.id')
    # Product.objects.filter(id=pro_id).delete()
    # return redirect(reverse('at:product_manage'))
    product_id = request.GET['product_id']
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


# 单接口管理
def apis_manage(request):
    apis_list = Apis.objects.all()
    paginator = Paginator(apis_list, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '接口用例管理',
        'apis_list': page_object,
    }

    return render(request, 'apis_manage.html', context=data)


# 添加单接口
def add_apis(request):
    if request.method == 'GET':

        pro_names = Product.objects.all()

        data = {
            'title': '添加接口用例',
            'pro_names': pro_names,
        }

        return render(request, 'add_apis.html', context=data)

    elif request.method == 'POST':
        api_product = request.POST.get('dropdown')
        api_name = request.POST.get('api_name')
        api_url = request.POST.get('api_url')
        api_param_value = request.POST.get('api_param_value')
        api_method = request.POST.get('method_check')
        api_result = request.POST.get('api_result')
        api_status = request.POST.get('api_status')

        apis = Apis.objects.filter(api_name=api_name)

        if api_name == "" or apis.exists():
            return redirect(reverse('at:add_apis'))
        else:
            api = Apis()
            api.api_name = api_name
            api.api_url = api_url
            api.api_param_value = api_param_value
            api.api_method = api_method
            api.api_result = api_result
            api.api_status = api_status
            api.api_pro_id = api_product

            api.save()

            return redirect(reverse('at:apis_manage'))
    return redirect(reverse('at:add_apis'))


# 编辑接口
def apis_update(request):
    apis_id = request.GET.get("apis.id")
    pro_names = Product.objects.all()
    apis = Apis.objects.filter(id=apis_id).first()

    data = {
        'title': '编辑接口用例',
        'apis': apis,
        'pro_names': pro_names,

    }

    if request.method == "POST":
        api_product = request.POST.get('dropdown')
        api_name = request.POST.get('api_name')
        api_url = request.POST.get('api_url')
        api_param_value = request.POST.get('api_param_value')
        api_method = request.POST.get('method_check')
        api_result = request.POST.get('api_result')
        api_status = request.POST.get('api_status')

        if api_name == "":
            return redirect(reverse('at:apis_update'))

        Apis.objects.filter(id=apis_id).update(
            api_name=api_name,
            api_url=api_url,
            api_param_value=api_param_value,
            api_method=api_method,
            api_result=api_result,
            api_status=api_status,
            api_pro_id=api_product
        )

        return redirect(reverse("at:apis_manage"))

    return render(request, 'apis_update.html', context=data)


# 删除接口
def apis_delete(request):
    apis_id = request.GET['apis_id']
    try:
        apis = Apis.objects.get(id=apis_id)
        apis.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


# 流程接口管理
def api_test_manage(request):
    api_test = Apitest.objects.all()
    paginator = Paginator(api_test, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '流程用例管理',
        'api_test': page_object,
    }

    return render(request, 'api_test_manage.html', context=data)


# 添加流程接口
def add_api_test(request):
    if request.method == "GET":

        pro_names = Product.objects.all()

        data = {
            'title': '添加接口用例',
            'pro_names': pro_names,
        }

        return render(request, 'add_api_test.html', context=data)
    elif request.method == "POST":
        api_product = request.POST.get('dropdown')
        api_t_name = request.POST.get('api_t_name')
        api_t_desc = request.POST.get('api_t_desc')
        api_ter = request.POST.get('api_ter')
        api_status = request.POST.get('api_status')

        api_tests = Apitest.objects.filter(api_t_name=api_t_name)

        if api_t_name == "" or api_tests.exists():
            return redirect(reverse('at:add_api_test'))
        else:
            api_test = Apitest()
            api_test.api_t_name = api_t_name
            api_test.api_t_desc = api_t_desc
            api_test.api_ter = api_ter
            api_test.api_t_res = api_status
            api_test.api_t_pro_id = api_product

            api_test.save()

            return redirect(reverse('at:api_test_manage'))
    return redirect(reverse('at:add_api_test'))


# 删除接口
def api_delete(request):
    api_id = request.GET['api_id']
    try:
        api = Apitest.objects.get(id=api_id)
        api.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


# 编辑接口
def api_update(request):
    api_id = request.GET.get("api_t.id")
    pro_names = Product.objects.all()
    api_t = Apitest.objects.filter(id=api_id).first()

    data = {
        'title': '编辑接口用例',
        'api_t': api_t,
        'pro_names': pro_names,

    }

    if request.method == "POST":
        api_product = request.POST.get('dropdown')
        api_t_name = request.POST.get('api_t_name')
        api_t_desc = request.POST.get('api_t_desc')
        api_ter = request.POST.get('api_ter')
        api_status = request.POST.get('api_status')

        if api_t_name == "":
            return redirect(reverse('at:api_update'))

        Apitest.objects.filter(id=api_id).update(
            api_t_name=api_t_name,
            api_t_desc=api_t_desc,
            api_ter=api_ter,
            api_t_res=api_status,
            api_t_pro_id=api_product,
        )

        return redirect(reverse("at:api_test_manage"))

    return render(request, 'api_update.html', context=data)


# 流程接口步骤管理
def api_step_manage(request):
    api_test_id = request.GET.get('api_t.id')
    api_test = Apitest.objects.get(id=api_test_id)
    api_steps = Apistep.objects.all()

    data = {
        'title': '接口用例步骤管理',
        'api_steps': api_steps,
        'api_test': api_test,

    }

    return render(request, 'api_step_manage.html', context=data)


# 添加流程接口步骤
def add_api_step(request):
    if request.method == "GET":

        api_tests = Apitest.objects.all()

        data = {
            'title': '添加接口用例步骤',
            'api_tests': api_tests,
        }

        return render(request, 'add_api_step.html', context=data)
    elif request.method == "POST":
        api_t_id = request.POST.get('dropdown')
        api_step = request.POST.get('api_step')
        api_name = request.POST.get('api_name')
        api_url = request.POST.get('api_url')
        api_param_value = request.POST.get('api_param_value')
        api_method = request.POST.get('method_check')
        api_result = request.POST.get('api_result')
        api_status = request.POST.get('api_status')

        if api_name == "":
            return redirect(reverse('at:add_api_step'))
        else:
            api_steps = Apistep()
            api_steps.api_name = api_name
            api_steps.api_step = api_step
            api_steps.api_url = api_url
            api_steps.api_param_value = api_param_value
            api_steps.api_method = api_method
            api_steps.api_result = api_result
            api_steps.api_status = api_status
            api_steps.api_test_id = api_t_id

            api_steps.save()

            return redirect(reverse('at:api_test_manage'))
    return redirect(reverse('at:add_api_step'))


# 删除接口步骤
def api_step_delete(request):
    api_step_id = request.GET['api_step_id']
    try:
        api_step = Apistep.objects.get(id=api_step_id)
        api_step.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


# 编辑接口步骤
def api_step_update(request):
    api_step_id = request.GET.get("api_step.id")
    api_tests = Apitest.objects.all()
    api_step = Apistep.objects.filter(id=api_step_id).first()

    data = {
        'title': '编辑接口用例',
        'api_step': api_step,
        'api_tests': api_tests,

    }

    if request.method == "POST":
        api_t_id = request.POST.get('dropdown')
        api_step = request.POST.get('api_step')
        api_name = request.POST.get('api_name')
        api_url = request.POST.get('api_url')
        api_param_value = request.POST.get('api_param_value')
        api_method = request.POST.get('method_check')
        api_result = request.POST.get('api_result')
        api_status = request.POST.get('api_status')

        if api_name == "":
            return redirect(reverse('at:api_step_update'))

        Apistep.objects.filter(id=api_step_id).update(
            api_name=api_name,
            api_step=api_step,
            api_url=api_url,
            api_param_value=api_param_value,
            api_method=api_method,
            api_result=api_result,
            api_status=api_status,
            api_test_id=api_t_id
        )

        return redirect(reverse("at:api_test_manage"))

    return render(request, 'api_step_update.html', context=data)


# bug管理
def bug_manage(request):
    bugs = Bug.objects.all()
    paginator = Paginator(bugs, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': 'Bug列表',
        'bugs': page_object,
    }

    return render(request, 'bug_manage.html', context=data)


# 添加bug
def add_bug(request):
    if request.method == "GET":

        pro_names = Product.objects.all()

        data = {
            'title': '添加Bug',
            'pro_names': pro_names,
        }

        return render(request, 'add_bug.html', context=data)
    elif request.method == "POST":
        bug_product = request.POST.get('dropdown')
        bug_name = request.POST.get('bug_name')
        bug_detail = request.POST.get('bug_detail')
        bug_level = request.POST.get('bug_level')
        bug_status = request.POST.get('bug_status')
        bug_creat_er = request.POST.get('bug_creat_er')
        bug_assign = request.POST.get('bug_assign')

        if bug_name == "":
            return redirect(reverse('at:add_bug'))
        else:
            bugs = Bug()
            bugs.bug_name = bug_name
            bugs.bug_detail = bug_detail
            bugs.bug_level = bug_level
            bugs.bug_status = bug_status
            bugs.bug_creat_er = bug_creat_er
            bugs.bug_assign = bug_assign
            bugs.bug_pro_id = bug_product

            bugs.save()

            return redirect(reverse('at:bug_manage'))
    return redirect(reverse('at:add_bug'))


# 删除bug
def bug_delete(request):
    bug_id = request.GET['bug_id']
    try:
        bug = Bug.objects.get(id=bug_id)
        bug.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 编辑bug
def bug_update(request):
    bug_id = request.GET.get("bug.id")
    pro_names = Product.objects.all()
    bug = Bug.objects.filter(id=bug_id).first()

    data = {
        'title': '编辑Bug',
        'bug': bug,
        'pro_names': pro_names,

    }

    if request.method == "POST":
        bug_product = request.POST.get('dropdown')
        bug_name = request.POST.get('bug_name')
        bug_detail = request.POST.get('bug_detail')
        bug_level = request.POST.get('bug_level')
        bug_status = request.POST.get('bug_status')
        bug_creat_er = request.POST.get('bug_creat_er')
        bug_assign = request.POST.get('bug_assign')

        if bug_name == "":
            return redirect(reverse('at:add_bug'))

        Bug.objects.filter(id=bug_id).update(
            bug_name=bug_name,
            bug_detail=bug_detail,
            bug_level=bug_level,
            bug_status=bug_status,
            bug_creat_er=bug_creat_er,
            bug_assign=bug_assign,
            bug_pro_id=bug_product,
        )

        return redirect(reverse("at:bug_manage"))

    return render(request, 'bug_update.html', context=data)


# 设置管理
def set_manage(request):
    sets = Set.objects.all()
    paginator = Paginator(sets, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '公共设置',
        'sets': page_object,
    }

    return render(request, 'set_manage.html', context=data)


# 用户设置管理
def set_user_manage(request):
    at_user = ATUser.objects.all()
    paginator = Paginator(at_user, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '用户管理',
        'at_user': page_object,
    }

    return render(request, 'set_user_manage.html', context=data)


# 添加管理
def add_set(request):
    if request.method == 'GET':

        data = {
            'title': '添加设置'
        }

        return render(request, 'add_set.html', context=data)
    elif request.method == 'POST':
        set_name = request.POST.get('set_name')
        set_value = request.POST.get('set_value')

        sets = Set.objects.filter(set_name=set_name)

        if set_name == "" or sets.exists():
            return redirect(reverse('at:add_set'))
        else:
            set_ = Set()
            set_.set_name = set_name
            set_.set_value = set_value

            set_.save()

            return redirect(reverse('at:set_manage'))
    return redirect(reverse('at:add_set'))


# App用例管理
def app_test_manage(request):
    app_tests = Apptest.objects.all()
    paginator = Paginator(app_tests, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': 'App用例管理',
        'app_tests': page_object,
    }

    return render(request, 'app_test_manage.html', context=data)


# 添加App用例
def add_app_test(request):
    if request.method == "GET":

        pro_names = Product.objects.all()

        data = {
            'title': '添加App用例',
            'pro_names': pro_names
        }

        return render(request, 'add_app_test.html', context=data)
    elif request.method == "POST":
        app_product = request.POST.get('dropdown')
        app_t_name = request.POST.get('app_t_name')
        app_t_desc = request.POST.get('app_t_desc')
        app_ter = request.POST.get('app_ter')
        app_t_res = request.POST.get('app_t_res')

        app_tests = Apptest.objects.filter(app_t_name=app_t_name)

        if app_t_name == "" or app_tests.exists():
            return redirect(reverse('at:add_app_test'))
        else:
            app_test = Apptest()
            app_test.app_t_name = app_t_name
            app_test.app_t_desc = app_t_desc
            app_test.app_ter = app_ter
            app_test.app_t_res = app_t_res
            app_test.app_t_pro_id = app_product

            app_test.save()

            return redirect(reverse('at:app_test_manage'))
    return redirect(reverse('at:add_app_test'))


# 删除app用例
def app_delete(request):
    app_id = request.GET['app_id']
    try:
        app = Apptest.objects.get(id=app_id)
        app.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 编辑app用例
def app_update(request):
    app_id = request.GET.get("app_t.id")
    pro_names = Product.objects.all()
    app_t = Apptest.objects.filter(id=app_id).first()

    data = {
        'title': '编辑App用例',
        'app_t': app_t,
        'pro_names': pro_names,

    }

    if request.method == "POST":
        app_product = request.POST.get('dropdown')
        app_t_name = request.POST.get('app_t_name')
        app_t_desc = request.POST.get('app_t_desc')
        app_ter = request.POST.get('app_ter')
        app_t_res = request.POST.get('app_t_res')

        if app_t_name == "":
            return redirect(reverse('at:app_update'))

        Apptest.objects.filter(id=app_id).update(
            app_t_name=app_t_name,
            app_t_desc=app_t_desc,
            app_ter=app_ter,
            app_t_res=app_t_res,
            app_t_pro_id=app_product
        )

        return redirect(reverse("at:app_test_manage"))

    return render(request, 'app_update.html', context=data)


# App用例步骤管理
def app_step_manage(request):
    app_t_id = request.GET.get('app_t.id')
    app_test = Apptest.objects.get(id=app_t_id)
    app_steps = Appteststep.objects.all()

    data = {
        'title': 'App用例步骤管理',
        'app_test': app_test,
        'app_steps': app_steps,
    }

    return render(request, 'app_step_manage.html', context=data)


# 添加App用例步骤
def add_app_step(request):
    if request.method == "GET":

        app_test = Apptest.objects.all()

        data = {
            'title': '添加App用例步骤',
            'app_test': app_test,
        }

        return render(request, 'add_app_step.html', context=data)
    elif request.method == "POST":
        app_t_id = request.POST.get('dropdown')
        app_step = request.POST.get('app_step')
        app_find_method = request.POST.get('app_find_method')
        app_element = request.POST.get('app_element')
        app_opt_method = request.POST.get('app_opt_method')
        app_test_data = request.POST.get('app_test_data')
        app_assert_data = request.POST.get('app_assert_data')
        app_result = request.POST.get('app_result')

        if app_step == "":
            return redirect(reverse('at:add_app_step'))
        else:
            app_steps = Appteststep()
            app_steps.app_step = app_step
            app_steps.app_find_method = app_find_method
            app_steps.app_element = app_element
            app_steps.app_opt_method = app_opt_method
            app_steps.app_test_data = app_test_data
            app_steps.app_assert_data = app_assert_data
            app_steps.app_result = app_result
            app_steps.app_test_id = app_t_id

            app_steps.save()

            return redirect(reverse('at:app_test_manage'))
    return redirect(reverse('at:add_app_step'))


# 删除App用例步骤
def app_step_delete(request):
    app_step_id = request.GET['app_step_id']
    try:
        app_step = Appteststep.objects.get(id=app_step_id)
        app_step.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 编辑App用例步骤
def app_step_update(request):
    app_step_id = request.GET.get("app_step.id")
    app_test = Apptest.objects.all()
    app_step = Appteststep.objects.filter(id=app_step_id).first()

    data = {
        'title': '编辑App用例步骤',
        'app_step': app_step,
        'app_test': app_test,

    }

    if request.method == "POST":
        app_t_id = request.POST.get('dropdown')
        app_step = request.POST.get('app_step')
        app_find_method = request.POST.get('app_find_method')
        app_element = request.POST.get('app_element')
        app_opt_method = request.POST.get('app_opt_method')
        app_test_data = request.POST.get('app_test_data')
        app_assert_data = request.POST.get('app_assert_data')
        app_result = request.POST.get('app_result')

        if app_step == "":
            return redirect(reverse('at:app_step_update'))

        Appteststep.objects.filter(id=app_step_id).update(
            app_step=app_step,
            app_find_method=app_find_method,
            app_element=app_element,
            app_opt_method=app_opt_method,
            app_test_data=app_test_data,
            app_assert_data=app_assert_data,
            app_result=app_result,
            app_test_id=app_t_id
        )

        return redirect(reverse("at:app_test_manage"))

    return render(request, 'app_step_update.html', context=data)


# Web用例管理
def web_test_manage(request):
    web_tests = Webtest.objects.all()
    paginator = Paginator(web_tests, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': 'Web用例管理',
        'web_tests': page_object,
    }

    return render(request, 'web_test_manage.html', context=data)


# 添加Web用例
def add_web_test(request):
    if request.method == "GET":

        pro_names = Product.objects.all()

        data = {
            'title': '添加Web用例',
            'pro_names': pro_names
        }

        return render(request, 'add_web_test.html', context=data)
    elif request.method == "POST":
        web_product = request.POST.get('dropdown')
        web_t_name = request.POST.get('web_t_name')
        web_t_desc = request.POST.get('web_t_desc')
        web_ter = request.POST.get('web_ter')
        web_t_res = request.POST.get('web_t_res')

        web_tests = Webtest.objects.filter(web_t_name=web_t_name)

        if web_t_name == "" or web_tests.exists():
            return redirect(reverse('at:add_web_test'))
        else:
            web_test = Webtest()
            web_test.web_t_name = web_t_name
            web_test.web_t_desc = web_t_desc
            web_test.web_ter = web_ter
            web_test.web_t_res = web_t_res
            web_test.web_t_pro_id = web_product

            web_test.save()

            return redirect(reverse('at:web_test_manage'))
    return redirect(reverse('at:add_web_test'))


# 删除web用例
def web_delete(request):
    web_id = request.GET['web_id']
    try:
        web = Webtest.objects.get(id=web_id)
        web.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 编辑web用例
def web_update(request):
    web_id = request.GET.get("web_t.id")
    pro_names = Product.objects.all()
    web_t = Webtest.objects.filter(id=web_id).first()

    data = {
        'title': '编辑Web用例',
        'web_t': web_t,
        'pro_names': pro_names,

    }

    if request.method == "POST":
        web_product = request.POST.get('dropdown')
        web_t_name = request.POST.get('web_t_name')
        web_t_desc = request.POST.get('web_t_desc')
        web_ter = request.POST.get('web_ter')
        web_t_res = request.POST.get('web_t_res')

        if web_t_name == "":
            return redirect(reverse('at:web_update'))

        Webtest.objects.filter(id=web_id).update(
            web_t_name=web_t_name,
            web_t_desc=web_t_desc,
            web_ter=web_ter,
            web_t_res=web_t_res,
            web_t_pro_id=web_product
        )

        return redirect(reverse("at:web_test_manage"))

    return render(request, 'web_update.html', context=data)


# Web用例步骤管理
def web_step_manage(request):
    web_t_id = request.GET.get('web_t.id')
    web_t = Webtest.objects.get(id=web_t_id)
    web_steps = Webteststep.objects.all()

    data = {
        'title': 'Web用例步骤管理',
        'web_t': web_t,
        'web_steps': web_steps,
    }

    return render(request, 'web_step_manage.html', context=data)


# 添加Web用例步骤
def add_web_step(request):
    if request.method == "GET":

        web_test = Webtest.objects.all()

        data = {
            'title': '添加Web用例步骤',
            'web_test': web_test,
        }

        return render(request, 'add_web_step.html', context=data)
    elif request.method == "POST":
        web_t_id = request.POST.get('dropdown')
        web_step = request.POST.get('web_step')
        web_find_method = request.POST.get('web_find_method')
        web_element = request.POST.get('web_element')
        web_opt_method = request.POST.get('web_opt_method')
        web_test_data = request.POST.get('web_test_data')
        web_assert_data = request.POST.get('web_assert_data')
        web_result = request.POST.get('web_result')

        if web_step == "":
            return redirect(reverse('at:add_web_step'))
        else:
            web_steps = Webteststep()
            web_steps.web_step = web_step
            web_steps.web_find_method = web_find_method
            web_steps.web_element = web_element
            web_steps.web_opt_method = web_opt_method
            web_steps.web_test_data = web_test_data
            web_steps.web_assert_data = web_assert_data
            web_steps.web_result = web_result
            web_steps.web_test_id = web_t_id

            web_steps.save()

            return redirect(reverse('at:web_test_manage'))
    return redirect(reverse('at:add_web_step'))


# web用例步骤删除
def web_step_delete(request):
    web_step_id = request.GET['web_step_id']
    try:
        web_step = Webteststep.objects.get(id=web_step_id)
        web_step.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# web用例步骤编辑
def web_step_update(request):
    web_step_id = request.GET.get("web_step.id")
    web_test = Webtest.objects.all()
    web_step = Webteststep.objects.filter(id=web_step_id).first()

    data = {
        'title': '编辑Web用例步骤',
        'web_step': web_step,
        'web_test': web_test,

    }

    if request.method == "POST":
        web_t_id = request.POST.get('dropdown')
        web_step = request.POST.get('web_step')
        web_find_method = request.POST.get('web_find_method')
        web_element = request.POST.get('web_element')
        web_opt_method = request.POST.get('web_opt_method')
        web_test_data = request.POST.get('web_test_data')
        web_assert_data = request.POST.get('web_assert_data')
        web_result = request.POST.get('web_result')

        if web_step == "":
            return redirect(reverse('at:web_step_update'))

        Webteststep.objects.filter(id=web_step_id).update(
            web_step=web_step,
            web_find_method=web_find_method,
            web_element=web_element,
            web_opt_method=web_opt_method,
            web_test_data=web_test_data,
            web_assert_data=web_assert_data,
            web_result=web_result,
            web_test_id=web_t_id
        )

        return redirect(reverse("at:web_test_manage"))

    return render(request, 'web_step_update.html', context=data)


# 接口报告
def apis_report(request):
    # 打开文件
    path = "E:/auto_test/apis_auto_test_case/report/"
    dirs = os.listdir(path)
    apis_list = []
    # 输出所有文件
    for file in dirs:
        apis_list.append(file)

    paginator = Paginator(apis_list, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '单一接口报告',
        'apis_list': page_object,
    }

    return render(request, 'apis_report.html', context=data)


def api_test_report(request):
    path = "E:/auto_test/api_test_auto_test_case/report/"
    dirs = os.listdir(path)
    api_test_list = []
    for file in dirs:
        api_test_list.append(file)

    paginator = Paginator(api_test_list, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': '流程接口报告',
        'api_test_list': page_object,
    }

    return render(request, 'api_test_report.html', context=data)


def web_report(request):
    path = "E:/auto_test/web_auto_test_case/report/"
    dirs = os.listdir(path)
    web_list = []
    for file in dirs:
        web_list.append(file)

    paginator = Paginator(web_list, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': 'Web测试报告',
        'web_list': page_object,
    }

    return render(request, 'web_report.html', context=data)


def app_report(request):
    path = "E:/auto_test/app_auto_test_case/report/"
    dirs = os.listdir(path)
    app_list = []
    for file in dirs:
        app_list.append(file)

    paginator = Paginator(app_list, 10)
    page = request.GET.get('page', 1)
    page_object = paginator.page(page)

    data = {
        'title': 'App测试报告',
        'app_list': page_object,
    }

    return render(request, 'app_report.html', context=data)


# 定时任务列表
def celery_manage(request):
    task_list = PeriodicTask.objects.all()
    # 周期任务（如一小时执行一次）
    periodic_list = IntervalSchedule.objects.all()
    # 定时任务（如某年某月某日，每天的某时）
    cron_list = CrontabSchedule.objects.all()

    data = {
        'title': '定时任务',
        'task_list': task_list,
        'periodic_list': periodic_list,
        'cron_list': cron_list,
    }

    return render(request, 'celery_manage.html', context=data)


# 删除celery
def celery_delete(request):
    task_id = request.GET['task_id']
    try:
        task = PeriodicTask.objects.get(id=task_id)
        task.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


# 启动celery条件
def celery_page(request):
    data = {
        'title': '启动celery条件'
    }

    return render(request, 'celery_page.html', context=data)


# 产品搜索
def pro_search(request):
    search_name = request.GET.get('p_product_name', '')
    # icontains忽略大小写
    pro_list = Product.objects.filter(p_product_name__icontains=search_name)

    # 分页
    paginator = Paginator(pro_list, 10)
    page = request.GET.get('page', 1)
    pro_lists = paginator.page(page)

    data = {
        'title': '产品中心',
        'products': pro_lists,
        'search_name': search_name,

    }

    return render(request, 'product_manage.html', context=data)


# 用例搜索
def apis_search(request):
    search_name = request.GET.get('api_name')
    api_list = Apis.objects.filter(api_name__icontains=search_name)

    # 分页
    paginator = Paginator(api_list, 10)
    page = request.GET.get('page', 1)
    api_lists = paginator.page(page)

    data = {
        'title': '接口用例管理',
        'search_name': search_name,
        'apis_list': api_lists,
    }

    return render(request, 'apis_manage.html', context=data)


# 流程用例搜索
def api_test_search(request):
    search_name = request.GET.get('api_t_name')
    api_t_list = Apitest.objects.filter(api_t_name__contains=search_name)

    # 分页
    paginator = Paginator(api_t_list, 10)
    page = request.GET.get('page', 1)
    api_t_lists = paginator.page(page)

    data = {
        'title': '流程用例管理',
        'search_name': search_name,
        'api_test': api_t_lists,
    }

    return render(request, 'api_test_manage.html', context=data)


# Web用例搜索
def web_search(request):
    search_name = request.GET.get('web_t_name')
    web_t_list = Webtest.objects.filter(web_t_name__contains=search_name)

    # 分页
    paginator = Paginator(web_t_list, 10)
    page = request.GET.get('page', 1)
    web_lists = paginator.page(page)

    data = {
        'title': 'Web用例管理',
        'web_tests': web_lists,
        'search_name': search_name,
    }

    return render(request, 'web_test_manage.html', context=data)


def app_search(request):
    search_name = request.GET.get('app_t_name')
    app_t_list = Apptest.objects.filter(app_t_name__contains=search_name)

    # 分页
    paginator = Paginator(app_t_list, 10)
    page = request.GET.get('page', 1)
    app_lists = paginator.page(page)

    data = {
        'title': 'App用例管理',
        'app_tests': app_lists,
        'search_name': search_name,
    }

    return render(request, 'app_test_manage.html', context=data)


def bug_search(request):
    search_name = request.GET.get('bug_name')
    bug_list = Bug.objects.filter(bug_name__contains=search_name)

    # 分页
    paginator = Paginator(bug_list, 10)
    page = request.GET.get('page', 1)
    bug_lists = paginator.page(page)

    data = {
        'title': 'App用例管理',
        'search_name': search_name,
        'bugs': bug_lists,
    }

    return render(request, 'bug_manage.html', context=data)


# 持续集成页面
def jenkins_page(request):
    data = {
        'title': 'jenkins页面'
    }

    return render(request, 'jenkins_page.html', context=data)


# 性能测试页面
def locust_page(request):
    data = {
        'title': 'locust页面'
    }

    return render(request, 'locust_page.html', context=data)


# Celery测试
def do(request):
    # 执行异步任务
    print('start do...')
    ApiTask.delay()
    print('end do...')
    return JsonResponse({'result': 'ok'})
