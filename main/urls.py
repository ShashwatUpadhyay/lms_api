from django.urls import path
from . import views



urlpatterns = [
    # teachers
    path('teacher/', views.TeacherList.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view()),
    path('teacher/dashboard/<int:pk>/', views.TeacherDashboard.as_view()),
    path('instructor-login/',views.TeacherLogin),
    path('instructor-verify/<str:full_name>/',views.verity_teacher_via_otp),
    path('teacher-forgot-password/',views.teacher_forgot_password),
    path('teacher-change-password/<str:full_name>/',views.teacher_change_password),
    # categoty
    path('category/',views.categoryList.as_view()),
    # cource
    path('cource/',views.courceList.as_view()),
    
    #spefic cource
    path('cource/<slug:slug>/',views.SpecificCourceList.as_view()),
   
    path('chapter/<slug:slug>/',views.ChapterUpdate.as_view()),
    path('chapter/',views.ChapterList.as_view()),
    #videos of specfic cource
    path('cource-chapter/<slug:slug>/',views.CourceChapterList.as_view()),
     #teacher cources
    path('teacher-cource/<int:teacher_id>',views.TeacherCourceList.as_view()),
    #Teacher of specfic cource
    path('teacher-cource-detail/<slug:slug>/',views.TeacherCourceUpdate.as_view()),
    
    #student 
    # path('student/', views.StudentList.as_view()),
    path('student/', views.user_register),
    path('student/<str:full_name>/', views.Student.as_view()),
    path('studenti/<int:pk>/', views.Student2.as_view()),
    path('student-login/',views.StudentLogin),
    path('verify/<str:full_name>/',views.verity_student_via_otp),
    path('student-forgot-password/',views.student_forgot_password),
    path('student-change-password/<str:full_name>/',views.student_change_password),
    path('student-cource-enroll/', views.StudentCourceEnrollList.as_view()),
    path('fetch-enroll-status/<int:student_id>/<slug:slug>/',views.fetch_enroll_status),
    path('fetch-enrolled-students/<slug:slug>/',views.enrolled_students_list.as_view()),
    path('fetch-all-enrolled-students/<int:teacher_id>',views.enrolled_students_list.as_view()),
    path('fetch-enrolled-cources/<int:student_id>/',views.enrolled_students_list.as_view()),
    path('add-favorite-cources/',views.StudentFavoriteCourceList.as_view()),
    path('remove-favorite-cources/<int:cource_id>/<int:student_id>/',views.remove_favorite_cource),
    path('fetch-favorite-cources/<int:student_id>/<int:cource_id>/',views.fetch_favorite_status),
    path('blog/',views.Blog.as_view()),
    path('blog/<slug:slug>/',views.BlogDetail.as_view()),
    path('user-assignment/<int:teacher_id>/<str:full_name>/',views.AssignmentList.as_view()),
    path('my-assignment/<int:student_id>/',views.MyAssignmentList.as_view()),
    path('update-assignment/<str:title>/',views.UpdateAssignment.as_view()),
    path('student/fetch-all-notification/<int:student_id>/',views.NotificationList.as_view()),
    path('save-notification/',views.NotificationListAll.as_view()),
    path('save-notification/<int:student_id>/',views.NotificationList.as_view()),
    #------------------Training-------------------#
    path('training/', views.TrainingList.as_view()),
    path('training/<slug:slug>/',views.SpecificTrainingList.as_view()),
    path('student-training-enroll/', views.StudentTrainingEnrollList.as_view()),
    path('fetch-training-enrolled-students/<slug:slug>/',views.training_enrolled_students_list.as_view()),
    path('fetch-training-enroll-status/<int:student_id>/<slug:slug>/',views.fetch_training_enroll_status),
    path('fetch-all-training-enrolled-students/<int:teacher_id>',views.training_enrolled_students_list.as_view()),
    path('fetch-enrolled-training/<int:student_id>/',views.training_enrolled_students_list.as_view()),
    path('teacher-training/<int:teacher_id>',views.TeacherTrainingList.as_view()),
    path('training-chapter/<slug:slug>/',views.TrainingChapterList.as_view()),
    path('training-chapters/<slug:slug>/',views.TrainingChapterListAll.as_view()),
    path('training-chapters-upload/<slug:slug>/',views.TrainingChapterUpload.as_view()),
    path('edit-training-chapter/<slug:slug>/',views.TrainingChapterUpdate.as_view()),
    path('delete-training-chapter/<slug:slug>/',views.TrainingChapterDelete.as_view()),
    path('user-training-assignment/<int:teacher_id>/<str:full_name>/',views.TrainingAssignmentList.as_view()),
    # path('my-training-assignment/<int:student_id>/',views.MyAssignmentList.as_view()),
    
    # payment
    path('pay/', views.start_payment, name="payment"),
    path('payment/success/', views.handle_payment_success, name="payment_success"),
    
    #Generate invoice
    path('invoice/<str:order_id>/', views.GenerateInvoice.as_view(), name="invoice"),
    

]  
