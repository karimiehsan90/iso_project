import math

import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *

def save(request,filename):
    file = request.FILES[filename]
    fs = FileSystemStorage()
    fn = fs.save(file.name,file)
    url = fs.url(fn)
    return url

def min(a,b):
    if a < b:
        return a
    return b
# Create your views here.
def index(request):
    createView(request)
    posts = Post.objects.all().reverse()
    ps = list(posts)
    ps.sort(key=lambda x:x.id,reverse=True)
    m = min(6,len(ps))
    ps = ps[0:m]
    return render(request,'main/index.html',{'posts' : ps})


def new_post(request):
    createView(request)
    e = ''
    if request.user.is_authenticated:
        title  = request.POST.get('title',None)
        pic = request.FILES.get('pic',None)
        if pic and title:
            url = save(request,'pic')
            Photo.objects.create(name=title,location=url)
            e = 'added'
        else:
            e = pic
    return render(request,'main/new_post.html',{'e' : e})

POST_PER_PAGE = 10
def blog(request):
    createView(request)
    page = request.GET.get('page',1);
    page = int(page)
    posts = Post.objects.all().reverse()
    pages = math.ceil(posts.count() / POST_PER_PAGE)
    pages = range(1,pages + 1)
    posts = list(posts)
    posts.sort(key=lambda x:x.id,reverse=True)
    first = POST_PER_PAGE * (page - 1)
    second = POST_PER_PAGE * page
    posts = posts[first:second]
    return render(request,'main/blog.html',{'posts':posts,'page':page,'page_pre':page - 1,'page_next':page + 1,'pages':pages})
def post(request,pid):
    createView(request)
    p = Post.objects.get(id=pid)
    return render(request,'main/post.html',{'p':p})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def createView(request):
    View.objects.create(ip=get_client_ip(request))

def status(request):
    createView(request)
    if request.user.is_authenticated:
        dt = datetime.datetime.now()
        day = dt.day
        month = dt.month
        year = dt.year
        status_day = []
        status_month = []
        status_year = []
        status_hour = []
        for i in range(1,day + 1):
            status_day.append({'value':View.objects.filter(date__year=year,date__month=month,date__day=i).count(),'key':i})
        for j in range(1,month + 1):
            status_month.append({'value':View.objects.filter(date__year=year,date__month=j).count(),'key':j})
        for i in range(2018,year + 1):
            status_year.append({'value':View.objects.filter(date__year=i).count(),'key':i})
        for i in range(1,25):
            status_hour.append({'key':i,'value':View.objects.filter(date__hour=i).count()})
        return render(request,'main/status.html',{'days':status_day,'monthes':status_month,'years':status_year,'hours':status_hour})
    return redirect('/')