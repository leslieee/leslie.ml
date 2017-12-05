# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
import models 
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
import json
from htmlhelper import pagerhelper
import os
import time
import threading
from django import forms
import socket
import commands

msg_dic={}


class DjangoUploadFileForm(forms.Form):
    username = forms.CharField()
    headimg = forms.FileField()

def upload(request):
    upload_list = models.DjangoUploadFile.objects.all()
    if request.method == "POST":
        uf = DjangoUploadFileForm(request.POST, request.FILES)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            headimg = uf.cleaned_data['headimg']
            user = models.DjangoUploadFile()
            user.username = username
            user.headimg = headimg
            user.save()
            #return HttpResponse('upload success.<br/>%s<br/>http://leslie.ml/upload/%s' % (username,headimg))
            #re = 'upload success.<br/>%s<br/>http://leslie.ml/uploads/%s' % (username,headimg)
            return render_to_response('upload_success.html',{'username':username,'filename':headimg,'upload_list':upload_list})
    else:
        uf = DjangoUploadFileForm()
    return render_to_response('upload.html',{'uf':uf,'upload_list':upload_list})

def poweroff():
    for i in range(5):
        time.sleep(1)
        os.system('shutdown -r now')

def fs_restart_thread():
    os.system('sh /fs/restart.sh')

def fs_restart(request):
    #output = os.popen('sh /fs/restart.sh').read()
    #os.system('sh /fs/start.sh')
    #os.system('nohup /fs/start.sh &')
    #t = threading.Thread(target=fs_restart_thread)
    #t.start()

    port=8081
    host='localhost'
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(b'hello,this is a test info !',(host,port))

    time.sleep(0.5)
    com = commands.getstatusoutput('ps -ef | grep fs.jar | grep -v grep')

    return HttpResponse(str(com))

def fs_start(request):
    os.system('sh /fs/start.sh')
    return HttpResponse('fs_start success.')

def fs_stop(request):
    os.system('sh /fs/stop.sh')
    return HttpResponse('fs_stop success.')

def reboot(request):
    #t = threading.Thread(target=poweroff)
    #t.start()
    os.system('reboot')
    return HttpResponse('reboot success.')

def acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username,password=password)
    print username,password
    if user is not None: #and user.is_active:
        #correct password and user is marked "active"
        auth.login(request,user)
        content = '''
        Welcome %s !!!
        
        <a href='/logout/' >Logout</a>
        
         ''' % user.username
        #return HttpResponse(content)
        return HttpResponseRedirect('/')
    else:
        return render_to_response('login.html',{'login_err':'Wrong username or password!'})
    

def logout_view(request):
    user = request.user
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponse("<b>%s</b> logged out! <br/><a href='/index/'>Re-login</a>" % user)


def Login(request):
    return render_to_response('login.html')



def index(request):
    bbs_list = models.BBS.objects.all()
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html', {
                                             'bbs_list':bbs_list,
                                             'user':request.user,
                                             'bbs_category':bbs_categories,
                                             'cata_id': 0})



def category(request,cata_id):
    bbs_list = models.BBS.objects.filter(category__id=cata_id)
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html',
                               {'bbs_list':bbs_list,
                                 'user':request.user,
                                 'bbs_category':bbs_categories,
                                 'cata_id': int(cata_id),
                              })



def bbs_detail(request, bbs_id):
    bbs = models.BBS.objects.get(id=bbs_id)
    print '--->', bbs
   
    return render_to_response('bbs_detail.html', {'bbs_obj':bbs,'user':request.user})
    
def sub_comment(request):
    print  request.POST
    bbs_id = request.POST.get('bbs_id')
    comment = request.POST.get('comment_content')
    
    
    
    comments.models.Comment.objects.create(
            content_type_id = 7,
            object_pk= bbs_id,
            site_id = 1,
            user = request.user,                       
            comment =   comment,                   
                                   )
    return  HttpResponseRedirect('/detail/%s' % bbs_id) 


def bbs_sub(request):
    print ',==>', request.POST.get('content')
    content=  request.POST.get('content')
    author = models.BBS_user.objects.get(user__username=request.user)
    category = models.Category.objects.get(name='审查')
    models.BBS.objects.create(
        title = 'TEST TITLE',
        summary = 'HAHA',
        content = content,
        author =author,
        category = category,
        view_count= 1,
        ranking = 1,                 
           )

    return HttpResponse('yes.')
def bbs_pub(request):
    return render_to_response('bbs_pub.html')


@login_required
def room(request,id):
    roomobj = models.ChatRoom.objects.get(id=id)
    result = models.ChatAccount.objects.filter(room=roomobj,user=request.user).count()
    if not result:
        c = models.ChatAccount(room=roomobj,user=request.user)
        c.save()
    memberlist = models.ChatAccount.objects.filter(room=roomobj)
    return render_to_response('room.html',{'roomobj':roomobj,'memberlist':memberlist,'user':request.user})

def savemsg(request):
    roomid,id,msg,sendtime,name = request.POST.get('roomid'), request.POST.get('id'),request.POST.get('msg'),request.POST.get('sendtime'),request.POST.get('name')

    if msg_dic.has_key(int(roomid)):
        msg_dic[int(roomid)].append([id,msg,sendtime,name])
    else:
         msg_dic[int(roomid)] = [[id,msg,sendtime,name],]

    return HttpResponse('OK')

def getmsg(request):
    roomid = request.GET.get('roomid')
    msglist = []
    if msg_dic.has_key(int(roomid)):
        msglist = msg_dic[int(roomid)]
    return HttpResponse(json.dumps(msglist))

def pager(request, page=1):
    # for i in range(100):
    #     userinfo = models.UserInfo(Name='alex'+str(i),Email='alex@live.com'+str(i),Phone='3838438'+str(i))
    #     userinfo.save()
    # return  HttpResponse('OK')

    page = int(page)
    totalnum = models.UserInfo.objects.all().count()
    p = pagerhelper.page('/pager/', totalnum, page)
    return render_to_response('pager.html',{'page':p})


























    
