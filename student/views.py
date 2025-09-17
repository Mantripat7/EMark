from django.shortcuts import render , redirect
# from teachers.models import _details 
from django.contrib import messages
from teacher.models import *
from datetime import datetime
# Create your views here.

def home(request):
    return render(request,'home.html')


def student_login_render(request):
    if request.method == "POST":
        data = request.POST
        try:
            qs = students_detials.objects.all().filter(roll_no = data.get("roll_no"))

            if (qs.values()[0]["roll_no"] == int(data.get("roll_no")) and qs.values()[0]["password"]==data.get("password")):
                request.session["login_data"] = qs.values()[0]
                return redirect('/student-home/')

            else:
                redirect("/student-login/")
                messages.warning(request, "Kindly Check Roll No and Password ")


        except IndexError:
            redirect("/student-login/")
            messages.warning(request, "Kindly Check Roll No and Password")
            
    return render(request,"student_login.html")

def student_home_render(request):
    try:
        login_data  = request.session["login_data"]
        stu_data = students_detials.objects.filter(roll_no=request.session['login_data']['roll_no']).values()[0]
        print(stu_data)
        stu_attend = 'empty'
        if attendence.objects.filter(roll_no=request.session['login_data']['roll_no'] , date=datetime.now().strftime('%Y-%m-%d')).exists():
            stu_attend = attendence.objects.filter(roll_no=request.session['login_data']['roll_no'] , date=datetime.now().strftime('%Y-%m-%d')).values()
        print(stu_attend)
    except TypeError:
       return redirect("/student-login/")
    
    context = {
        "login_data": login_data,
        "stu_data": stu_data,
        "stu_attend":stu_attend,
    }
    return render(request,"student_home.html",context)
