from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,permissions
from . import models
from .serializers import TeacherSerializer,TrainingSerializer,OrderSerializer,StudentTrainingAssignmentSerializer,StudentTrainingEnrollSerializer,TrainingChapterSerializer, CategorySerializer,NotificationSerializer,StudentSerializerTwo,StudentAssignmentSerializer,CourceSerializer,StudentFavoriteCourceSerializer,ChapterSerializer, StudentSerializer,StudentEnrollSerializer,TeacherDashboardSerializer,BlogSerializer,StudentSerializerForProfile
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
from random import randint
from rest_framework.decorators import api_view
from rest_framework.response import Response
import environ
import razorpay
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from io import BytesIO
from django.views import View
import random
# Create your views here.

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None


class GenerateInvoice(View):
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = models.Order.objects.get(order_id=order_id)
            print(order)
        except Exception as e:
            print(e)
            return HttpResponse("505 Not Found")
        data = {
            'user': order.user.full_name,
            'user_email': order.user.email,
            'order_product': order.order_product.title,
            'order_amount': order.order_amount,
            'order_id': order.order_id,
            'order_date': order.order_date,
            'isPaid': order.isPaid,
            'transaction_id': order.order_payment_id,
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type = 'application/pdf')
            
class TeacherList(generics.ListCreateAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [permissions.IsAuthenticated]
    

        
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
@csrf_exempt
def TeacherLogin(request):
    email= request.POST['email']
    password= request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(email=email,password=password)
    except models.Teacher.DoesNotExist:
        teacherData=None
    if teacherData:
        if not teacherData.login_via_otp:
            return  JsonResponse({'bool':True,'teacher_id': teacherData.id,'full_name': teacherData.full_name, 'msg':'success'})
        else:
            otp_digit = randint(1000,9999)
            send_mail(
            'Verify Account',
            'Please Verify Your Account',
            'shashwat.allswift@gmail.com',
            [teacherData.email],
            fail_silently=False,
            html_message=f"<p>Your OTP is </p>{otp_digit}</p>"
        )    
        models.Teacher.objects.filter(email=email,password=password).update(otp_digit=otp_digit)
        return  JsonResponse({'bool':True, 'login_via_otp': True,'full_name': teacherData.full_name}) 
    else:
        return JsonResponse({'bool':False, 'msg':'Please enter valid otp'})
    
@csrf_exempt
def verity_teacher_via_otp(request,full_name):
    otp_digit = request.POST.get('otp_digit')
    verify = models.Teacher.objects.filter(full_name=full_name,otp_digit=otp_digit).first()
    if verify:
        models.Teacher.objects.filter(full_name=full_name,otp_digit=otp_digit).update(verify_status=True)
        return JsonResponse({'bool':True,'teacher_id': verify.id, 'full_name':verify.full_name})
        # if verify.login_via_otp:
        #     return JsonResponse({'bool':True, 'teacher_id': verify.id, 'login_via_otp':True})
        # else:   
        #     return JsonResponse({'bool':False, 'teacher_id': verify.id, 'login_via_otp':False})
    else:
            return JsonResponse({'bool':False, 'msg':'Please Enter valid 4 digit OTP'})
        
        
class categoryList(generics.ListCreateAPIView):
    queryset=models.CourceCategory.objects.all()
    serializer_class = CategorySerializer
    

class courceList(generics.ListCreateAPIView):
    queryset=models.Cource.objects.all()
    serializer_class = CourceSerializer
    
    def get_queryset(self):
        qs=  super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs =  models.Cource.objects.all().order_by('-id')[:limit]
        return qs
    
class SpecificCourceList(generics.RetrieveAPIView):
    queryset=models.Cource.objects.all()
    serializer_class = CourceSerializer
    lookup_field='slug'
    

class ChapterList(generics.ListCreateAPIView):
    queryset=models.Chapter.objects.all()
    serializer_class = ChapterSerializer    
    
class ChapterUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Chapter.objects.all()
    serializer_class = ChapterSerializer    
    lookup_field='slug'
    
# specific teacher cource
class TeacherCourceList(generics.ListAPIView):
    serializer_class = CourceSerializer 
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher= models.Teacher.objects.get(pk=teacher_id)
        return models.Cource.objects.filter(teacher=teacher)
    
    
class TeacherCourceUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Cource .objects.all()
    serializer_class = CourceSerializer
    lookup_field= 'slug'

#specific video of cource
class CourceChapterList(generics.ListAPIView):
    serializer_class = ChapterSerializer
    def get_queryset(self):
        cource_id = self.kwargs['slug']
        cource= models.Cource.objects.get(slug=cource_id)
        return models.Chapter.objects.filter(cource=cource)
    
#student detail

class StudentList(generics.ListCreateAPIView):
    queryset=models.Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    
class Student(generics.RetrieveUpdateAPIView):
    queryset=models.Student.objects.all()
    serializer_class = StudentSerializerTwo
    lookup_field='full_name'
    
@csrf_exempt
def user_register(request):
    queryset=models.Student.objects.all()
    serializer_class = StudentSerializerTwo
    email = request.POST.get('email')
    full_name = request.POST.get('full_name')
    mobile_no = request.POST.get('mobile_no')
    dob = request.POST.get('dob')
    password = request.POST.get('password')
    college = request.POST.get('college')
    year= request.POST.get('year')
    state = request.POST.get('state')
    city= request.POST.get('city')
    department= request.POST.get('department')
    domain= request.POST.get('domain')
    refer_code= request.POST.get('refer_code')
    login_via_otp= request.POST.get('login_via_otp')
    student_data = {
        'full_name': full_name,
        'email': email,
        'password': password,  # Save the password safely (use hashing in production)
        'mobile_no': mobile_no,  # Save the password safely (use hashing in production)
        'dob': dob,  # Save the password safely (use hashing in production)
        'college': college,  # Save the password safely (use hashing in production)
        'year': year,  # Save the password safely (use hashing in production)
        'department': department,  # Save the password safely (use hashing in production)
        'state': state,  # Save the password safely (use hashing in production)
        'city': city,  # Save the password safely (use hashing in production)
        'domain': domain,  # Save the password safely (use hashing in production)
        'refer_code': refer_code,  # Assuming there’s a ForeignKey to ReferCode in the Student model
        'otp_digit': 0,  # Assuming there’s a ForeignKey to ReferCode in the Student model
    }
    
    try:
        if models.Student.objects.get(email = email):
            return  JsonResponse({'bool':False,'msg':'This email already exist '})
    except models.Student.DoesNotExist as e:
        print(e)
    
    try:
        refer = models.ReferCode.objects.get(code = refer_code)
    except models.ReferCode.DoesNotExist:
        return  JsonResponse({'bool':False,'msg':'You must have valid Refer code'})
    
    try:
        models.Student.objects.create(**student_data)
        return JsonResponse({'bool': True, 'msg': 'Thank you for Registration!!'})
    except Exception as e:
        return JsonResponse({'bool': False, 'msg': 'Something Went Wrong!!'})
        
    # serializer = StudentSerializer(data=student_data)
    # if serializer.is_valid():
    #     serializer.save()  # Save the new student to the database
    #     return JsonResponse({'bool': True, 'msg': 'Thank you for Registration!!'})
    # else:
    #     # If serializer validation fails, return errors
    #     return JsonResponse({'bool': False, 'msg': 'Registration failed', 'errors': serializer.errors})
    
class Student2(generics.RetrieveUpdateAPIView):
    queryset=models.Student.objects.all()
    serializer_class = StudentSerializerForProfile
    # permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def StudentLogin(request):
    email= request.POST['email']
    password= request.POST['password']
    try:
        studentData = models.Student.objects.get(email=email,password=password)
    except models.Student.DoesNotExist:
        studentData=None
      
    if studentData:
        if not studentData.login_via_otp:
            return  JsonResponse({'bool':True,'student_id': studentData.id,'full_name':studentData.full_name ,'msg':'success'})
        else:
            otp_digit = randint(1000,9999)
            send_mail(
            'Verify Account',
            'Please Verify Your Account',
            'shashwat.allswift@gmail.com',
            [studentData.email],
            fail_silently=False,
            html_message=f"<p>Your OTP is </p>{otp_digit}</p>"
        )    
        models.Student.objects.filter(email=email,password=password).update(otp_digit=otp_digit)
        return  JsonResponse({'bool':True, 'login_via_otp': True,'full_name': studentData.full_name}) 
    else:
        return JsonResponse({'bool':False, 'msg':'Please enter valid otp'})  
      
    # if studentData:
    #     return  JsonResponse({'bool':True, 'student_id':studentData.id}) 
    # else:
    #     return JsonResponse({'bool':False})
    
    
@csrf_exempt
def verity_student_via_otp(request,full_name):
    otp_digit = request.POST.get('otp_digit')
    verify = models.Student.objects.filter(full_name=full_name,otp_digit=otp_digit).first()
    if verify:
        models.Student.objects.filter(full_name=full_name,otp_digit=otp_digit).update(verify_status=True, otp_digit = random.randint(1000,9999))
        return JsonResponse({'bool':True,'student_id': verify.id,'full_name': verify.full_name})
        # if verify.login_via_otp:
        #     return JsonResponse({'bool':True, 'teacher_id': verify.id, 'login_via_otp':True})
        # else:   
        #     return JsonResponse({'bool':False, 'teacher_id': verify.id, 'login_via_otp':False})
    else:
            return JsonResponse({'bool':False, 'msg':'Please Enter valid 4 digit OTP'})
        


class StudentCourceEnrollList(generics.ListCreateAPIView):
    queryset=models.StudentCourceEnrollment.objects.all()
    serializer_class = StudentEnrollSerializer

def fetch_enroll_status(request,student_id,slug):
    student = models.Student.objects.filter(id=student_id).first()
    cource = models.Cource.objects.filter(slug=slug).first()
    enrollStatus=models.StudentCourceEnrollment.objects.filter(cource=cource,student=student).count()
    if enrollStatus:
        return  JsonResponse({'bool':True}) 
    else:
        return JsonResponse({'bool':False})
    
class enrolled_students_list(generics.ListAPIView):
    queryset=models.StudentCourceEnrollment.objects.all()
    serializer_class = StudentEnrollSerializer
    lookup_field = 'slug'
    
    
    def get_queryset(self):
        if 'slug' in self.kwargs:   
            cource_id = self.kwargs['slug']
            cource= models.Cource.objects.get(slug=cource_id)
            return models.StudentCourceEnrollment.objects.filter(cource=cource)
        elif 'teacher_id' in self.kwargs:
            teacher_id=self.kwargs['teacher_id']
            teacher = models.Teacher.objects.get(pk=teacher_id)
            return models.StudentCourceEnrollment.objects.filter(cource__teacher=teacher).distinct()
        elif 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student = models.Student.objects.get(pk=student_id)
            return models.StudentCourceEnrollment.objects.filter(student=student).distinct()

class TeacherDashboard(generics.RetrieveAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class=TeacherDashboardSerializer
            
class StudentFavoriteCourceList(generics.ListCreateAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class=StudentFavoriteCourceSerializer

def fetch_favorite_status(request,student_id,cource_id):
    student = models.Student.objects.filter(id=student_id).first()
    cource = models.Cource.objects.filter(id=cource_id).first()
    favoriteStatus=models.FavoriteCource.objects.filter(cource=cource,student=student).count()
    if favoriteStatus:
        return  JsonResponse({'bool':True}) 
    else:
        return JsonResponse({'bool':False})
    
def remove_favorite_cource(request,cource_id,student_id):
    student = models.Student.objects.filter(id=student_id).first()
    cource = models.Cource.objects.filter(id=cource_id).first()
    favoriteStatus=models.FavoriteCource.objects.filter(cource=cource,student=student).delete()
    if favoriteStatus:
        return  JsonResponse({'bool':True}) 
    else:
        return JsonResponse({'bool':False})
    
    
#-----------------------Blog-------------------------------------#

class Blog(generics.ListCreateAPIView):
    queryset=models.blog.objects.all().order_by('-update_time')
    serializer_class = BlogSerializer
    
    def get_queryset(self):
        qs=  super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs =  models.blog.objects.all().order_by('-update_time')[:limit]
        return qs
    
class BlogDetail(generics.RetrieveAPIView):
    queryset=models.blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field='slug'
#-----------------------Blog End-------------------------------------#
    
    
    
#-----------------------assignment-------------------------------------#
    
class AssignmentList(generics.ListCreateAPIView):
    queryset=models.Assignments.objects.all()
    serializer_class = StudentAssignmentSerializer
    
    def get_queryset(self):
        full_name = self.kwargs['full_name']
        teacher_id = self.kwargs['teacher_id']
        student= models.Student.objects.get(full_name=full_name)
        teacher= models.Teacher.objects.get(pk=teacher_id)
        return models.Assignments.objects.filter(student=student,teacher=teacher)
    
class AssignmentList(generics.ListCreateAPIView):
    queryset=models.Assignments.objects.all()
    serializer_class = StudentAssignmentSerializer
    
    def get_queryset(self):
        full_name = self.kwargs['full_name']
        student= models.Student.objects.get(full_name=full_name)
        return models.Assignments.objects.filter(student=student)
    
class MyAssignmentList(generics.ListCreateAPIView):
    queryset=models.Assignments.objects.all()
    serializer_class = StudentAssignmentSerializer
    lookup_field='full_name'
    
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student= models.Student.objects.get(pk=student_id)
        models.Notification.objects.filter(student=student,notif_for='student',notif_subject='assignment').update(notif_status=True)
        return models.Assignments.objects.filter(student=student)
    
        
class UpdateAssignment(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Assignments.objects.all()
    serializer_class = StudentAssignmentSerializer
    lookup_field = 'title'
#-----------------------assignment End-------------------------------------#
    
class NotificationListAll(generics.ListCreateAPIView):
    queryset=models.Notification.objects.all()
    serializer_class = NotificationSerializer
    
class NotificationList(generics.ListCreateAPIView):
    queryset=models.Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        student_id =self.kwargs['student_id']
        student = models.Student.objects.get(pk=student_id)
        return models.Notification.objects.filter(student=student,notif_for='student',notif_subject='assignment',notif_status=False)
        

#-----------------------TRAINING-------------------------------------#
class TrainingList(generics.ListCreateAPIView):
    queryset=models.Training.objects.all()
    serializer_class = TrainingSerializer
    
    def get_queryset(self):
        qs=  super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs =  models.Training.objects.all().order_by('-id')[:limit]
        return qs
    
class SpecificTrainingList(generics.RetrieveAPIView):
    queryset=models.Training.objects.all()
    serializer_class = TrainingSerializer 
    lookup_field = 'slug'
    
# class ChapterList(generics.ListCreateAPIView):
#     queryset=models.TrainingChapter.objects.all()
#     serializer_class = TrainingChapterSerializer
    
class TrainingChapterUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.TrainingChapter.objects.all()
    serializer_class = TrainingChapterSerializer 
    lookup_field = 'slug'
    
class TeacherTrainingList(generics.ListAPIView):
    serializer_class = TrainingSerializer 
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher= models.Teacher.objects.get(pk=teacher_id)
        return models.Training.objects.filter(teacher=teacher)
    
class TeacherTrainingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Training.objects.all()
    serializer_class = TrainingSerializer
    
class TrainingChapterList(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.TrainingChapter.objects.all()
    serializer_class = TrainingChapterSerializer    
    lookup_field='slug'
    
class TrainingChapterUpload(generics.CreateAPIView):
    queryset=models.TrainingChapter.objects.all()
    serializer_class = TrainingChapterSerializer    
    lookup_field='slug'

class TrainingChapterListAll(generics.ListAPIView):
    serializer_class = TrainingChapterSerializer
    def get_queryset(self):
        cource_id = self.kwargs['slug']
        cource= models.Training.objects.get(slug=cource_id)
        return models.TrainingChapter.objects.filter(training=cource)
    

class TrainingChapterDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrainingChapterSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        slug = self.kwargs['slug']
        return models.TrainingChapter.objects.filter(slug=slug)
   
    
class StudentTrainingEnrollList(generics.ListCreateAPIView):
    queryset=models.StudentTrainingEnrollment.objects.all()
    serializer_class = StudentTrainingEnrollSerializer

def fetch_training_enroll_status(request,student_id,slug):
    student = models.Student.objects.filter(id=student_id).first()
    training = models.Training.objects.filter(slug=slug).first()
    enrollStatus=models.StudentTrainingEnrollment.objects.filter(training=training,student=student).count()
    if enrollStatus:
        return  JsonResponse({'bool':True}) 
    else:
        return JsonResponse({'bool':False})
    
class training_enrolled_students_list(generics.ListAPIView):
    queryset=models.StudentTrainingEnrollment.objects.all()
    serializer_class = StudentTrainingEnrollSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        if 'slug' in self.kwargs:
            training_id = self.kwargs['slug']
            training= models.Training.objects.get(slug=training_id)
            return models.StudentTrainingEnrollment.objects.filter(training=training)
        elif 'teacher_id' in self.kwargs:
            teacher_id=self.kwargs['teacher_id']
            teacher = models.Teacher.objects.get(pk=teacher_id)
            return models.StudentTrainingEnrollment.objects.filter(training__teacher=teacher).distinct()
        elif 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student = models.Student.objects.get(pk=student_id)
            return models.StudentTrainingEnrollment.objects.filter(student=student).distinct()
        
class TrainingAssignmentList(generics.ListCreateAPIView):
    queryset=models.TrainingAssignments.objects.all()
    serializer_class = StudentTrainingAssignmentSerializer
    
    def get_queryset(self):
        full_name = self.kwargs['full_name']
        teacher_id = self.kwargs['teacher_id']
        student= models.Student.objects.get(full_name=full_name)
        teacher= models.Teacher.objects.get(id=teacher_id)
        return models.TrainingAssignments.objects.filter(student=student,teacher=teacher)
        



#-----------------------TRAINING-------------END------------------------#

@csrf_exempt
def teacher_forgot_password(request):
    email = request.POST.get('email')
    verify = models.Teacher.objects.filter(email=email).first()
    if verify:
        link = f"http://localhost:5173/instructor-change-password/{verify.full_name}/"
        send_mail(
            'Forgot Password',
            'Change Password',
            'shashwat.allswift@gmail.com',
            [email],
            fail_silently=False,
            html_message=f"<p>Click  <a href='{link}'>here</a> to change your password"
        )
        return JsonResponse({'bool':True,'msg':"Email Sent! Please check your email"})
    else:
            return JsonResponse({'bool':False, 'msg':'Invalid Email'})
    
@csrf_exempt
def teacher_change_password(request,full_name):
    password = request.POST.get('password')
    verify = models.Teacher.objects.filter(full_name=full_name).first()
    if verify:
        verify = models.Teacher.objects.filter(full_name=full_name).update(password=password)
        return JsonResponse({'bool':True,'msg':"Password changed!"})
    else:
            return JsonResponse({'bool':False, 'msg':'Something Went Wrong'})
        
    
@csrf_exempt
def student_forgot_password(request):
    email = request.POST.get('email')
    verify = models.Student.objects.filter(email=email).first()
    if verify:
        link = f"http://localhost:5173/change-password/{verify.full_name}/"
        send_mail(
            'Forgot Password',
            'Change Password',
            'shashwat.allswift@gmail.com',
            [email],
            fail_silently=False,
            html_message=f"<p>Click  <a href='{link}'>here</a> to change your password"
        )
        return JsonResponse({'bool':True,'msg':"Email Sent! Please check your email"})
    else:
            return JsonResponse({'bool':False, 'msg':'Invalid Email'})
    
    
@csrf_exempt
def student_change_password(request,full_name):
    password = request.POST.get('password')
    verify = models.Student.objects.filter(full_name=full_name).first()
    if verify:
        verify = models.Student.objects.filter(full_name=full_name).update(password=password)
        return JsonResponse({'bool':True,'msg':"Password changed!"})
    else:
            return JsonResponse({'bool':False, 'msg':'Something Went Wrong'})
      

# payment gateway

env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']
    user = request.data['user']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    student_instance = models.Student.objects.get(id=int(user))
    cource_instance = models.Cource.objects.get(id=int(name))
    order = models.Order.objects.create(user = student_instance,
                                        order_product=cource_instance, 
                                        order_amount=amount, 
                                        order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = models.Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)
    print(check)
    if check is not None:
        print("Redirect to error url or error page")
        return JsonResponse({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)
