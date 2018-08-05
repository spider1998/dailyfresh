#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from . import user_decorator
from df_goods.models import GoodsInfo

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断密码
    if upwd!=upwd2:
        return redirect('/user/register')
    #密码加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    #注册成功转到登录页
    return redirect('/user/login/')

def register_exit(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    users=UserInfo.objects.filter(uname=uname)
    print uname
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')
            red=HttpResponseRedirect(url)
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        context={'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

@user_decorator.login
def info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_list1=goods_ids.split(',')
    goods_list=[]
    for goods_id in goods_list1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context={
        'title':'用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name'],
        'goods_list':goods_list
    }
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    context={'title':'用户中心','user_name':request.session['user_name']}
    return render(request, 'df_user/user_center_order.html', context)

@user_decorator.login
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.youbian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={
        'title':'用户中心',
        'user':user,
        'user_name': request.session['user_name']
    }
    return render(request,'df_user/user_center_site.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')














