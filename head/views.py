from django.shortcuts import render , redirect
from head.models import *
from teacher.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime

def send_mail_to_client(msg):
    subject = "This Email Is sent from Django Server"
    message = msg
    from_email = settings.EMAIL_HOST_USER
    recipients_list = ['raghav2002asr@gmail.com']
    send_mail(subject, message, from_email ,recipients_list)

def admin_login(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        database_email = admin_details.objects.all()[0].email
        database_pass = admin_details.objects.all()[0].password

        if(email == database_email and password == database_pass):
                print('Login successful')
                request.session["data"] = email
                return redirect('/admin-home/')
        else:
            print('Login failed')

    return render(request,'pages-login.html')

def admin_home(request):
            try:
               data = request.session["data"]
               # Getting the Today's Lect. Data and sending to the dashboard
               if datetime.now().strftime("%A")=='Monday':
                    upcoming_lect=btech_cse_time_table.objects.values_list('subject1','subject2','subject3','subject4','subject5')[0]
               elif datetime.now().strftime("%A")=='Tuesday':
                    upcoming_lect = btech_cse_time_table.objects.values_list('subject6','subject7','subject8','subject9','subject10')[0]
               elif datetime.now().strftime("%A")=='Wednesday':
                    upcoming_lect = btech_cse_time_table.objects.values_list('subject11','subject12','subject13','subject14','subject15')[0]
               elif datetime.now().strftime("%A")=='Thursday':
                    upcoming_lect = btech_cse_time_table.objects.values_list('subject16','subject17','subject18','subject19','subject20')[0]
               elif datetime.now().strftime("%A")=='Friday':
                    upcoming_lect = btech_cse_time_table.objects.values_list('subject21','subject22','subject23','subject24','subject25')[0]
               else:
                    upcoming_lect = ('NO LECT')

               # Counting the number of Lect and attendence
               subject_list = list(set(btech_cse_time_table.objects.values_list('subject1','subject2','subject3','subject4','subject5','subject6','subject7','subject8','subject9','subject10','subject11','subject12','subject13','subject14','subject15','subject16','subject17','subject18','subject19','subject20','subject21','subject22','subject23','subject24','subject25')[0]))
               subject_list.remove('')
               dates_set = set(attendence.objects.values_list("date"))
               roll_no_set =set(attendence.objects.values_list('roll_no'))
               i=0
               total_lect = {}
               while i<len(subject_list):        
                    count = 0             
                    for date in dates_set:
                         if attendence.objects.filter(date=date[0],subject=subject_list[i]).exists():
                              count += 1
                    total_lect[subject_list[i]] = count
                    i=i+1

               attended_lect = []
               r=-1
               for roll in roll_no_set:
                    j=0
                    r=r+1
                    attended_lect.append([attendence.objects.filter(roll_no=roll[0]).values()[0]['fullname'],roll[0]])
                    while j<len(subject_list):                 
                         count_attendence=attendence.objects.filter(roll_no=roll[0],subject=subject_list[j],attend='present').count()
                         attended_lect[r].append(count_attendence)
                         j=j+1
               print(attended_lect)



               context = {
                    'teacher_data': teacher_details.objects.all(),
                    'upcoming_lect': upcoming_lect,
                    'lect_time': btech_cse_time_table.objects.values_list('time1','time2','time3','time4','time5')[0],
                    'total_lect': total_lect,
                    'attended_lect':attended_lect,
                 "data": data,
            }
               return render(request,'index.html',context)
            except TypeError:
                 return redirect('/admin-login/')

def teacher_detail(request):
     try:
          request.session["data"]
          if request.method == 'POST':
                for i in range(len(teacher_details.objects.all())):
                      print(teacher_details.objects.all()[i].email)
                      if (teacher_details.objects.all()[i].email == request.POST.get('email')):
                            messages.success(request, "Teacher With same email address already exists")
                            return redirect('/teacher-details/')
                teacher =  teacher_details(fullname = request.POST.get('fullname'),email = request.POST.get('email'),address = request.POST.get('address'), phone = request.POST.get('phone'),subject= request.POST.get('subject'),password = request.POST.get('password'))
                teacher.save()
                messages.success(request, "Teacher Added Successfully")
                send_mail_to_client(f"You have been registered to eMarkBook ✨. Now you can login to teacher dashboard 💫🌟. Your username and password are : {request.POST.get('email')} and {request.POST.get('password')}")
                return redirect('/teacher-details/')
          return render(request,'teacher_details.html',context = {'teacher_details':teacher_details.objects.all()})

     except KeyError:
          return redirect('/admin-login/')    


def delete_teacher(request,email):
    print(f"Deleting teacher whose email is : {email} --------------->")
    del_teacher = teacher_details.objects.filter(email=email)
    del_teacher.delete()
    return redirect('/teacher-details/')


def update_teacher_details_function(request,email):
    if request.method == 'POST':
         print(email)
         data = request.POST
         teacher = teacher_details.objects.filter(email=email)[0]
         print(teacher)
         teacher.status = data.get('status')
         teacher.save()
    return redirect('/teacher-details/')

def time_table_render(request):
     try:
          request.session["data"]    
          if request.method == 'POST':
                data =  request.POST
                new_time_table = btech_cse_time_table(day = data.get('day'),
                                                time1 = data.get('time1'),
                                                time2 = data.get('time2'),
                                                time3 = data.get('time3'),
                                                time4 = data.get('time4'),
                                                time5 = data.get('time5'),
                                                monday = data.get('monday'),
                                                tuesday = data.get('tuesday'),
                                                wednesday = data.get('wednesday'),
                                                thursday = data.get('thursday'),
                                                friday = data.get('friday'),
                                                subject1 = data.get('subject1'),
                                                subject2 = data.get('subject2'),
                                                subject3 = data.get('subject3'),
                                                subject4 = data.get('subject4'),
                                                subject5 = data.get('subject5'),
                                                subject6 = data.get('subject6'),
                                                subject7 = data.get('subject7'),
                                                subject8 = data.get('subject8'),
                                                subject9 = data.get('subject9'),
                                                subject10 = data.get('subject10'),
                                                subject11 = data.get('subject11'),
                                                subject12 = data.get('subject12'),
                                                subject13 = data.get('subject13'),
                                                subject14 = data.get('subject14'),
                                                subject15 = data.get('subject15'),
                                                subject16 = data.get('subject16'),
                                                subject17 = data.get('subject17'),
                                                subject18 = data.get('subject18'),
                                                subject19 = data.get('subject19'),
                                                subject20 = data.get('subject20'),
                                                subject21 = data.get('subject21'),
                                                subject22 = data.get('subject22'),
                                                subject23 = data.get('subject23'),
                                                subject24 = data.get('subject24'),
                                                subject25 = data.get('subject25'))
                new_time_table.save()
          try:
               data = btech_cse_time_table.objects.all().values()[0]
               num=1
          except:
               num = 0
               data= "no data"
          return render(request,'time_table.html', context={'data':data,'num':num})
     except TypeError:
          return redirect('/admin-login/')


def update_time_table_render(request,id):
     if request.method == 'POST':
          data = request.POST
          del_time_table = btech_cse_time_table.objects.filter(id=id)
        #   print(f"getting the data from update time table : {upd_time_table.values()}")
          updated_time_table = btech_cse_time_table(day = data.get('day'),
                                                time1 = data.get('time1'),
                                                time2 = data.get('time2'),
                                                time3 = data.get('time3'),
                                                time4 = data.get('time4'),
                                                time5 = data.get('time5'),
                                                monday = data.get('monday'),
                                                tuesday = data.get('tuesday'),
                                                wednesday = data.get('wednesday'),
                                                thursday = data.get('thursday'),
                                                friday = data.get('friday'),
                                                subject1 = data.get('subject1'),
                                                subject2 = data.get('subject2'),
                                                subject3 = data.get('subject3'),
                                                subject4 = data.get('subject4'),
                                                subject5 = data.get('subject5'),
                                                subject6 = data.get('subject6'),
                                                subject7 = data.get('subject7'),
                                                subject8 = data.get('subject8'),
                                                subject9 = data.get('subject9'),
                                                subject10 = data.get('subject10'),
                                                subject11 = data.get('subject11'),
                                                subject12 = data.get('subject12'),
                                                subject13 = data.get('subject13'),
                                                subject14 = data.get('subject14'),
                                                subject15 = data.get('subject15'),
                                                subject16 = data.get('subject16'),
                                                subject17 = data.get('subject17'),
                                                subject18 = data.get('subject18'),
                                                subject19 = data.get('subject19'),
                                                subject20 = data.get('subject20'),
                                                subject21 = data.get('subject21'),
                                                subject22 = data.get('subject22'),
                                                subject23 = data.get('subject23'),
                                                subject24 = data.get('subject24'),
                                                subject25 = data.get('subject25')
               
          )
          updated_time_table.save()
          del_time_table.delete()

     return redirect("/time-table/")