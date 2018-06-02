from django.shortcuts import render, HttpResponse, redirect
from .forms import SendMsgForm, UserInfoForm, LoginForm
from . import models
from django.core.mail import send_mail
from django.db.models import Q
import json, datetime
import io
# Create your views here.


class BaseResponse(object):
    def __init__(self, *args, **kwargs):
        self.status = False
        self.summary = None
        self.error = None
        self.data = None

def index(request):
    
    return render(request, 'index.html')


def sendMsg(request):
    
    obj = BaseResponse()
    form = SendMsgForm(request.POST)
    if form.is_valid():
        value_dict = form.clean()
        email = value_dict['email']
        has_exists_email = models.UserInfo.objects.filter(email = email).count()
        if has_exists_email:
            obj.summary = '此邮箱已被注册'
            return HttpResponse(json.dumps(obj.__dict__))
        
        current_date = datetime.datetime.now()
        import random
        yzm = str(int(random.random()*10000))

        count = models.SendMsg.objects.filter(email = email).count()
        
        if not count:
            models.SendMsg.objects.create(email=email, code=yzm, stime=current_date)
            obj.status = True
            send_mail('验证码', yzm, '946085650@qq.com', [
                 '946085650@qq.com'], fail_silently=False)
        else:
            limit_date = current_date - datetime.timedelta(hours=1)
            times = models.SendMsg.objects.filter(email=email, stime__gt=limit_date, times__gt=9).count()
            if times:
                obj.summary = "已超过最大次数(1小时后重试)"
            else:
                unfreeze = models.SendMsg.objects.filter(email=email, stime__lt=limit_date).count()
                if unfreeze:
                    models.SendMsg.objects.filter(email=email).update(times=0)    
                from django.db.models import F
                models.SendMsg.objects.filter(email=email).update(code=yzm, stime=current_date, times=F('times')+1)
                obj.status = True
                send_mail('验证码', yzm, '946085650@qq.com', ['946085650@qq.com'], fail_silently=False)
    else:
        obj.summary = form.errors['email'][0]
    return HttpResponse(json.dumps(obj.__dict__))


def register(request):
    obj = BaseResponse()
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            current_data = datetime.datetime.now()
            limit_date = current_data - datetime.timedelta(minutes=1)
            value_dict = form.clean()
            id_code_valid = models.SendMsg.objects.filter(email=value_dict['email'], code=value_dict['code'], stime__gt=limit_date).count()
            if not id_code_valid:
                print('验证码过期')
            else:
                if(models.UserInfo.objects.filter(username=value_dict['username'])):
                    obj.summary("用户名被已被注册")
                if(models.UserInfo.objects.filter(email=value_dict['password'])):
                    print('邮箱已被注册')
                models.UserInfo.objects.create(
                    username=value_dict['username'], email=value_dict['email'], pwd=value_dict['password'])
                models.SendMsg.objects.filter(email=value_dict['email']).delete()
        else:
            obj.error = form.errors
    return HttpResponse(obj.__dict__)


def login(request):

    obj = BaseResponse()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            value_dict = form.clean()
            if value_dict['code'].upper() == request.session['CheckCode']:
                if models.UserInfo.objects.filter(Q(Q(username=value_dict['username']), Q(pwd=value_dict['password'])) | Q(
                    Q(email=value_dict['username']), Q(pwd=value_dict['password']))):
                    obj.status = True
                    request.session['is_login'] = True
                    request.session['username'] = value_dict['username']
                else:
                    obj.summary = '用户名或密码错误'
            else:
                obj.summary = '验证码错误'
        else:
            obj.error = form.errors

    return HttpResponse(json.dumps(obj.__dict__))


def check_code(request):
    from .backend import check_code
    stream = io.BytesIO()
    img, code = check_code.create_code()
    img.save(stream, "png")
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('index')
    request.session.flush()
    return redirect('index')

