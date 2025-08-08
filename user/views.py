import re

from django.shortcuts import render, redirect

# Create your views here.
from admins.models import UploadModel
from user.models import RegisterModel, SQLModel, WebsiteModel


def index(request):
    splt=''
    cls=[]
    pre=[]
    exe=[]
    ans=''
    usid=''
    pswd=''
    check=''
    qwe=''
    if request.method == "POST":
        usid = request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            check = RegisterModel.objects.get(userid=usid, password=pswd)
            request.session['userid'] = check.id
            return redirect('userpage')
        except:
            qwe=request.session['userid']
            splt = (re.findall(r"[\w']+", str(usid)))
            for a in splt:
                if a in ('UPDATE','SET','WHERE'):
                    cls.append(a)
                elif a in ('loginName','bob'):
                    pre.append(a)
                elif a in ('OR'):
                    exe.append(a)
            if len(cls) >= len(pre) and len(cls) > len(exe):
                ans="Clauses"
            elif len(pre) > len(cls) and len(pre) > len(exe):
                ans='Predicates'
            elif len(exe) >= len(cls) and len(exe) > len(pre):
                ans='Expressions'
            else:
                ans='No SQL Injection Attack'
        SQLModel.objects.create(attack_type=ans, text=usid)
    return render(request,'user/index.html',{'a':splt,'ans':ans})

def register(request):
    a = ''
    b = ''
    c = ''
    d = ''
    e = ''
    f = ''
    g = ''

    if request.method == "POST":
        a = request.POST.get('fname')
        b = request.POST.get('lname')
        c = request.POST.get('userid')
        d = request.POST.get('pword')
        e = request.POST.get('mblenum')
        f = request.POST.get('email')
        g = request.POST.get('gender')
        RegisterModel.objects.create(firstname=a, lastname=b, userid=c, password=d, mblenum=e, email=f, gender=g)
        return redirect('index')
    return render(request,'user/register.html')

def userpage(request):
    obj = UploadModel.objects.all()
    return render(request,'user/userpage.html',{'obj':obj})

def mydetails(request):
    usid = request.session['userid']
    us_id = RegisterModel.objects.get(id=usid)
    return render(request,'user/mydetails.html',{'obje':us_id})

def check_website(request):
    usid = request.session['userid']
    us_id = RegisterModel.objects.get(id=usid)
    a=''
    b=''
    ans=''
    if request.method =="POST":
        a=request.POST.get('feedback')
        b=a.split("/")
        for d in b:
            if d in ("1=1","UPDATE","SET","bob"):
                ans=" Attack Is Detected"
            else:
                ans="Attack Is Not Detected"
        WebsiteModel.objects.create(txt=a,rest=ans,usid=us_id)
    return render(request,'user/check_website.html',{'j':b,'we':ans})

def view_website(request):
    usid = request.session['userid']
    us_id = RegisterModel.objects.get(id=usid)
    onj=WebsiteModel.objects.filter(usid=us_id)

    return render(request,'user/view_website.html',{'obj':onj})