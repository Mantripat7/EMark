"""
URL configuration for emarkbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from head.views import *
from teacher.views import *
from student.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',home),


    # Teacher Route Starts
    path('teacher-login/',teacher_login_render),         #done
    path('teacher_home/',teacher_home_render),           #done
    # students 
    path('fill-stu-details/',teacher_fill_student_details_render),
    path('fill-stu-details/<roll_no>',delete_student_record_render),
    path('update-stu-details/<roll_no>',update_student_record_render),

    path('assignment-1_marks/',assignment_1_marks_render),     
    path('assignment-2_marks/',assignment_2_marks_render),     
    path('assignment-3_marks/',assignment_3_marks_render),       
    path('mst-1_marks/',mst_1_marks_render),
    path('mst-2_marks/',mst_2_marks_render),
    # changes
    path('attendence-marks/',attendence_render),             
    path('update-attendence/',update_attendence_render),

    # Admin Routes starts
    path('admin-home/',admin_home),
    path('admin-login/',admin_login),
    path('teacher-details/',teacher_detail),
    path('admin/', admin.site.urls),
    path('teacher-details/<email>',delete_teacher),
    path('update_teacher_details/<email>',update_teacher_details_function),
    path('time-table/',time_table_render),                #done
    path('time-table/<id>',update_time_table_render),   


    # Student routes
    path('student-login/',student_login_render),
    path('student-home/',student_home_render)
    # path('student-data/',student_data_render)
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)