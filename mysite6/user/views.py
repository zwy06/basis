from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User # 导入django中的User模型类


# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        return render(request,'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password1 = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        # 验证数据合法性
        if len(username) < 6:
            username_err = '用户名太短'
            return render(request,'user/register.html',locals())
        # 验证密码1不能为空
        if len(password1) == 0:
            password_err = '密码不能为空'
            return render(request,'user/register.html',locals())
        # 验证两次密码必须一致
        if password1 != password2:
            password2_err = '两次密码不一致'
            return render(request,'user/register.html',locals())
        try:
            auser = User.objects.get(username=username)
            username_err = '用户名已存在'
            return render(request,'user/register.html',locals())
        except Exception as err:
            # auser = User.objects.create_user(
            auser = User.objects.create_superuser(
                username=username,
                password=password1,
                email=''
            )
            auser.last_name = 'tedu'
            auser.save()
        html = "注册成功!<a href='/user/login'>进入登录</a>"
        resp = HttpResponse(html)
        # 添加cook
        resp.set_cookie('username',username)
        return resp

def login_view(request):
    if request.method == 'GET':
        username = request.COOKIES.get('username','')
        return render(request,'user/login.html',locals())
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username == '':
            username_err = '用户名不能为空'
            return render(request,'user/login.html',locals())
        try:
            auser = User.objects.get(username=username)
            # 记录一个登录状态
            if auser.check_password(password):
                request.session['user'] = {
                    'username':username,
                    'id':auser.id # 记录当前用户的id
                }
                resp = HttpResponseRedirect('/')
                if 'remeber' in request.POST: # 选中状态
                    resp.set_cookie('username',username)
                return resp
            else:
                password_err = '密码错误'
                return render(request,'user/login.html',locals())
        except Exception as err:
            password_err = '用户名或者密码不正确'
            return render(request,'user/login.html',locals())

def logout_view(request):
    if 'user' in request.session:
        del request.session['user'] # 清除登录记录
    return HttpResponseRedirect('/') # 返回首页

from . import forms
def reg2_view(request):
    if request.method == 'GET':
        myform1 = forms.MyRegForm()
        return render(request,'user/reg2.html',locals())
    elif request.method == 'POST':
        myform = forms.MyRegForm(request.POST)
        if myform.is_valid():
            dic = myform.cleaned_data
            username = dic['username']
            password = dic['password']
            password2 = dic['password2']
            return HttpResponse(str(dic))
        else:
            return HttpResponse('验证失败')

def change_pwd_view(request):
    if request.method == 'GET':
        myform1 = forms.MyChangePwdForm()
        return render(request,'user/change_pwd.html',locals())
    elif request.method == 'POST':
        myform = forms.MyChangePwdForm(request.POST)
        if myform.is_valid():
            dic = myform.cleaned_data
            username = dic['username']
            password_old = dic['password_old']
            password = dic['password']
            try:
                auser = User.objects.get(username = username)
                if auser.check_password(password_old):
                    auser.set_password(password)
                    auser.save()
                else:
                    err = '密码错误'
                    return render(request,'user/change_pwd.html',locals())
            except Exception as err:
                err = '用户名不对'
                return render(request,'user/change_pwd.html',locals())
            return HttpResponseRedirect('/user/login')



