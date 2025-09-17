from django.shortcuts import render , redirect
from teacher.models import *
from head.models import *
from django.contrib import messages
import cv2
from datetime import date
from json import dumps
from datetime import datetime
import sched,time
from deepface import DeepFace
# Create your views here.
scheduler = sched.scheduler(time.time,  
                            time.sleep) 

def teacher_login_render(request):
    if request.method == "POST":
        if(teacher_details.objects.filter(email = request.POST.get('email')).exists() and teacher_details.objects.filter(password = request.POST.get('password')).exists()):
            a = teacher_details.objects.filter(email = request.POST.get('email')).values()
            print(a)
            request.session["teacher_data"] = {
                "email":request.POST.get('email'),
                "name":a[0]["fullname"],
                "subject":a[0]["subject"],
                "status":a[0]["status"]
            }
            return redirect('/teacher_home/')
        else:
            messages.warning(request, "Kindly Check Email and Password ...")
            return redirect("/teacher-login/")
    return render(request,"teacher_login.html")

def teacher_home_render(request):
    try:
        login_data  = request.session["teacher_data"]
        dates_set = set(attendence.objects.values_list("date"))
        roll_no_set =set(attendence.objects.values_list('roll_no'))
        # Conunting the total number of lectures  
        count = 0           
        for date in dates_set:
            if attendence.objects.filter(date=date[0],subject=request.session['teacher_data']['subject']).exists():
                count += 1

        # Attended Lectures 
        attended_lect = []
        r=-1
        for roll in roll_no_set:
            r=r+1
            attended_lect.append([attendence.objects.filter(roll_no=roll[0]).values()[0]['fullname'],roll[0]])               
            stu_attendence=attendence.objects.filter(roll_no=roll[0],subject=request.session['teacher_data']['subject'],attend='present')
            count_attendence = stu_attendence.count()
            attended_lect[r].append(count_attendence)
        
        # MST-1 Toppers
        topper_1_mst_1 = 'No Data'
        topper_2_mst_1 = 'No Data'
        topper_3_mst_1 = 'No Data'
        failed_stu_mst_1= '0'
        if students_detials.objects.filter(subject=request.session['teacher_data']['subject']).order_by('mst_1_marks').exists() and students_detials.objects.filter(subject=request.session['teacher_data']['subject']).count()>3:
            toppers_mst_1  = students_detials.objects.filter(subject=request.session['teacher_data']['subject']).order_by('mst_1_marks').values()
            topper_1_mst_1 = toppers_mst_1[toppers_mst_1.count()-1]
            topper_2_mst_1 = toppers_mst_1[toppers_mst_1.count()-2]
            topper_3_mst_1 = toppers_mst_1[toppers_mst_1.count()-3]
            failed_stu_mst_1  = students_detials.objects.filter(mst_1_marks__lte =8).count()

        # MST-2 Toppers
        topper_1_mst_2 = 'No Data'
        topper_2_mst_2 = 'No Data'
        topper_3_mst_2 = 'No Data'
        failed_stu_mst_2= '0'
        if students_detials.objects.filter(subject=request.session['teacher_data']['subject']).order_by('mst_2_marks').exists() and students_detials.objects.filter(subject=request.session['teacher_data']['subject']).count()>3:
            toppers_mst_2  = students_detials.objects.filter(subject=request.session['teacher_data']['subject']).order_by('mst_2_marks').values()
            topper_1_mst_2 = toppers_mst_2[toppers_mst_2.count()-1]
            topper_2_mst_2 = toppers_mst_2[toppers_mst_2.count()-2]
            topper_3_mst_2 = toppers_mst_2[toppers_mst_2.count()-3]
            failed_stu_mst_2  = students_detials.objects.filter(mst_2_marks__lte =8).count()

        # Calculating Internel Marks
        internal_marks = []
        cal_internal_marks = []
        im = -1
        for stu in attended_lect:
            if students_detials.objects.filter(roll_no=stu[1],subject=request.session['teacher_data']['subject']).values().exists() and count>0:
                im=im+1
                student  = students_detials.objects.filter(roll_no=stu[1],subject=request.session['teacher_data']['subject']).values()[0]
                if(student['mst_1_marks']==None or student['mst_2_marks']==None or student['assignment_1_marks']==None or student['assignment_2_marks']==None or student['assignment_3_marks']==None):
                    internal_marks.append([student['fullname'],stu[1],student['mst_1_marks'],student['mst_2_marks'],student['assignment_1_marks'],student['assignment_2_marks'],student['assignment_3_marks'],None])
                else:
                    internal_marks.append([student['fullname'],stu[1],student['mst_1_marks'],student['mst_2_marks'],student['assignment_1_marks'],student['assignment_2_marks'],student['assignment_3_marks'],(student['mst_1_marks']+student['mst_2_marks'])/2 + (student['assignment_1_marks']+student['assignment_2_marks']+student['assignment_3_marks'])/3])
                if (int(stu[2])/count)*100 > 90.00:
                    r=6
                    internal_marks[im].append(6)
                elif 85.00 > (stu[2]/count)*100 < 90.00:
                    r=5
                    internal_marks[im].append(5)
                elif 80.00 > (stu[2]/count)*100 < 85.00:
                    r=4
                    internal_marks[im].append(4)
                elif 75.00 > (stu[2]/count)*100 < 80.00:
                    r=3
                    internal_marks[im].append(3)
                elif 75.00 > (stu[2]/count)*100:
                    r=0
                    internal_marks[im].append(0)
                if internal_marks[im][7] != None:
                    internal_marks[im][7] = round(internal_marks[im][7]+internal_marks[im][8],2)
                    if internal_marks[im][7] >= 16:
                        internal_marks[im].append('Pass')
                    else:
                        internal_marks[im].append('Fail')
                else:
                    internal_marks[im].append(None)
                temp = internal_marks[im][7]
                internal_marks[im][7] = internal_marks[im][8]
                internal_marks[im][8] = temp
            # internal_marks[im].pop(8)
            # internal_marks[im].append(r)
        print(internal_marks)
            
                


        return render(request,'teacher_home.html',context ={'teacher_data':login_data,'total_lect':count,'attended_lect':attended_lect,"topper_1_mst_1":topper_1_mst_1,"topper_2_mst_1":topper_2_mst_1,"topper_3_mst_1":topper_3_mst_1,"failed_stu_mst_1":failed_stu_mst_1,"topper_1_mst_2":topper_1_mst_2,"topper_2_mst_2":topper_2_mst_2,"topper_3_mst_2":topper_3_mst_2,"failed_stu_mst_2":failed_stu_mst_2,"internal_marks":internal_marks,'cal_internal_marks':cal_internal_marks})
    
    except KeyError:
        return redirect("/teacher-login/")

def mst_1_marks_render(request):
    try:
        login_data  = request.session["teacher_data"]
        print(login_data)
        if request.method == 'POST':
            for k, v in list(request.POST.items())[1:]:
                print(students_detials.objects.filter(roll_no=k).update(mst_1_marks=v))
        return render(request,'mst_1_marks.html',context={'marks_details':students_detials.objects.filter(subject=request.session['teacher_data']['subject']),'teacher_data':login_data})
    except KeyError:
        return redirect("/teacher-login/")

def mst_2_marks_render(request):
    try:
        login_data  = request.session["teacher_data"]
        print(login_data)
        if request.method == 'POST':
            for k, v in list(request.POST.items())[1:]:
                print(students_detials.objects.filter(roll_no=k).update(mst_2_marks=v))
        return render(request,'mst_2_marks.html',context={'marks_details':students_detials.objects.filter(subject=request.session['teacher_data']['subject']),'teacher_data':login_data})
    except KeyError:
        return redirect("/teacher-login/")


def assignment_1_marks_render(request):
    try:
        login_data  = request.session["teacher_data"]
        print(login_data)
        if request.method == 'POST':
            for k, v in list(request.POST.items())[1:]:
                print(students_detials.objects.filter(roll_no=k).update(assignment_1_marks=v))
        return render(request,'assignment_1_marks.html',context={'marks_details':students_detials.objects.filter(subject=request.session['teacher_data']['subject']),'teacher_data':login_data})
    except KeyError:
        return redirect("/teacher-login/")


def assignment_2_marks_render(request):
    try:
        login_data  = request.session["teacher_data"]
        print(login_data)
        if request.method == 'POST':
            for k, v in list(request.POST.items())[1:]:
                print(students_detials.objects.filter(roll_no=k).update(assignment_2_marks=v))
        return render(request,'assignment_2_marks.html',context={'marks_details':students_detials.objects.filter(subject=request.session['teacher_data']['subject']),'teacher_data':login_data})
    except KeyError:
        return redirect("/teacher-login/")

def assignment_3_marks_render(request):
    try:
        login_data  = request.session["teacher_data"]
        print(login_data)
        if request.method == 'POST':
            for k, v in list(request.POST.items())[1:]:
                print(students_detials.objects.filter(roll_no=k).update(assignment_3_marks=v))
        return render(request,'assignment_3_marks.html',context={'marks_details':students_detials.objects.filter(subject=request.session['teacher_data']['subject']),'teacher_data':login_data})
    except KeyError:
        return redirect("/teacher-login/")
    
present_stu_set = set()

def read_cam(students_data):
    url='http://192.0.0.4:8080/video'
    cam = cv2.VideoCapture(url)
    result,frame =cam.read()
    detect =  DeepFace.extract_faces(img_path=frame, detector_backend = 'mtcnn' ,enforce_detection =False)
    x = detect[0]['facial_area']['x']
    y = detect[0]['facial_area']['y']
    # print(detect)
    if x == 0 or y == 0 :
        print("No face detected")
    else:
        for stu in students_data:
            img1_path = f"media/{stu['image']}"
            result = DeepFace.verify(img1_path = img1_path,img2_path= frame,model_name = 'ArcFace', detector_backend = 'retinaface',enforce_detection=False)
            # result = DeepFace.verify(img1_path = img1_path,img2_path= frame,enforce_detection=False)
            if (result['verified'] == True):
                print(f"{stu['fullname']} is present")
                present_stu_set.add(stu['roll_no'])
            else:
                print(f"{stu['fullname']} is not present")

def attendence_render(request):
    try:
        login_data  = request.session["teacher_data"]
        update_wala_data = attendence.objects.filter(date = datetime.today().strftime("%Y-%m-%d"))

        if request.method == 'POST':
                    if attendence.objects.filter(date = datetime.today().strftime("%Y-%m-%d"),subject=request.session['teacher_data']['subject']).exists():
                         messages.warning(request,"Today's Attendence has been successfully taken if you want to update the attendence click on update attendence option")
                         return redirect('/attendence-marks/')
                    else:
                        # converting query set to list of dict
                        students_data = []
                        for stu in students_detials.objects.all().values():
                            students_data.append(stu)
                        print(students_data)


                        v=0
                        ctime = time.localtime().tm_min
                        while time.localtime().tm_min <  ctime+2:
                            present_stu_list = list(present_stu_set)
                            print(present_stu_list)
                            for present_stu in present_stu_list:
                                    if len(students_data)>0:
                                        while v < len(students_data):
                                            if students_data[v]['roll_no']==present_stu:
                                                del students_data[v]
                                            v=v+1
                                    else:
                                        break
                            scheduler.enter(5,1,read_cam,argument=(students_data,))
                            scheduler.run()


                        for stu in students_detials.objects.all().values():
                            attend= attendence(attend = "absent" , roll_no = stu['roll_no'] , date= date.today(),fullname =stu["fullname"],subject=request.session['teacher_data']['subject'])
                            attend.save()

                        for at_st in present_stu_list:
                                if  attendence.objects.filter( roll_no = at_st , date= date.today(),subject=request.session['teacher_data']['subject']).values().exists():
                                    
                                    attendence.objects.filter( roll_no = at_st , date= date.today(),subject=request.session['teacher_data']['subject']).update(attend = "present")
                                    

                        return redirect('/attendence-marks/')
        print(request.session['teacher_data']['subject'])
        data = dumps(list(attendence.objects.filter(subject=request.session['teacher_data']['subject']).values()),default=str)
        return render(request,'attendence.html', context={"attendence_data":data,'teacher_data':login_data,'update_wala_data': update_wala_data})
    except KeyError:
        return redirect("/teacher-login/")


def update_attendence_render(request):
    try:
        login_data  = request.session["teacher_data"]
        if request.method == 'POST':
            for k, v in list(request.POST.items())[1:]:
                attendence.objects.filter(id=k,subject=request.session['teacher_data']['subject']).update(attend = v)
        return redirect('/attendence-marks/')
    except KeyError:
        return redirect("/teacher-login/")

def teacher_fill_student_details_render(request):
    try:
        login_data  = request.session["teacher_data"]
        print(login_data)
        if request.method == 'POST':
            data = request.POST
            if students_detials.objects.filter(roll_no = data.get('roll_no')).exists():
                messages.warning(request,"Student with same roll no already exists")
                return redirect("/fill-stu-details/")
            else:
                data_to_database = students_detials(fullname=data.get("full_name"), roll_no=data.get("roll_no"),  phone=data.get("phone"), password=data.get("password"), email=data.get("email"), image=request. FILES.get("image"),subject=request.session['teacher_data']["subject"])
                data_to_database.save()
                messages.success(request,"Student record added successfully")
                return redirect("/fill-stu-details/")
        stu_details = students_detials.objects.filter(subject=request.session['teacher_data']['subject']).values()
        return render(request,'teacher_fill_stu_detail.html',context={'stu_details':stu_details,'teacher_data':login_data})
    except KeyError:
        return redirect("/teacher-login/")
    
def delete_student_record_render(request,roll_no):
    stu = students_detials.objects.filter(roll_no = roll_no , subject = request.session['teacher_data']['subject'])
    stu.delete()
    return redirect('/fill-stu-details/')

def update_student_record_render(request,roll_no):
    if request.method == 'POST':
        data = request.POST
        print(roll_no)
        stu = students_detials.objects.filter(roll_no = roll_no,subject = request.session['teacher_data']['subject'])
        if request.FILES.get('image') == None:
            stu.update(fullname=data.get("full_name"), phone=data.get("phone"),  email=data.get("email"))
            messages.success(request,"Student record updated successfully")
        else:
            passwords = stu.values()[0]["password"] 
            stu.delete()
            students_detials(fullname=data.get("full_name"),roll_no=roll_no, password=passwords, phone=data.get("phone"),  email=data.get("email"),image = request.FILES.get('image'),subject=request.session['teacher_data']['subject']).save()
            messages.success(request,"Student record updated successfully")
    
    return redirect('/fill-stu-details/')