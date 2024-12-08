from rest_framework import serializers
from . import models
from django.core.mail import send_mail


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields  = ['id','profile_img','full_name','email','skills','mobile_no','teacher_cource','login_via_otp','otp_digit']
        
    def __init__(self, *args, **kwargs):
        super(TeacherSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

    def create(self, validated_data):
        email = self.validated_data['email']
        otp_digit = self.validated_data['otp_digit']
        instance = super(TeacherSerializer,self).create(validated_data)
        send_mail(
            'Verify Account',
            'Please Verify Your Account',
            'shashwatup619@gmail.com',
            [email],
            fail_silently=False,
            html_message=f"<p>Your OTP is </p>{otp_digit}</p>"
        )
        return instance
            
class TeacherDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields= ['total_teacher_cource','total_teacher_chapter','total_teacher_student']

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourceCategory
        fields  = ['id','title','description']
        
class CourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cource
        fields  = ['id','title','slug','description','overview','category','thumbnail', 'requirement','price','teacher','cource_chapter','related_Cource','total_enrolled','add_time']
    
    def __init__(self, *args, **kwargs):
        super(CourceSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
        
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields  = ['id','cource','title','slug','description','video','add_time']
    # def __init__(self, *args, **kwargs):
    #     super(ChapterSerializer,self).__init__(*args, **kwargs)
    #     request=self.context.get('request')
    #     self.Meta.depth = 0
    #     if request and request.method == 'GET':
    #         self.Meta.depth = 1
        
   
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields  = ['id','full_name','email','password','mobile_no','dob','college','year','department','state','city','domain','refer_code','login_via_otp']
        
class StudentSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields  = ['id','full_name','email','mobile_no','college','year','department','state','city','domain','refer_code','login_via_otp']

class StudentSerializerForProfile(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields  = ['id','full_name','email','mobile_no','dob','registration_date','college','year','department','state','city','domain','login_via_otp']

        
class StudentEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCourceEnrollment  
        fields  = ['id','cource','student','enrolled_time']
        
    def __init__(self, *args, **kwargs):
        super(StudentEnrollSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            
class StudentFavoriteCourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavoriteCource  
        fields  = ['id','cource','student','status']
        
    def __init__(self, *args, **kwargs):
        super(StudentFavoriteCourceSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.blog  
        fields  = ['title','slug','desc','category','update_time','author','img1','article1','img2','article2']
    
    def __init__(self, *args, **kwargs):
        super(BlogSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogCategory
        fields  = ['id','title','description']

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assignments
        fields  = ['student','teacher','title','detail','student_status','add_time']
    
    def __init__(self, *args, **kwargs):
        super(StudentAssignmentSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2

class StudentTrainingAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrainingAssignments
        fields  = ['student','teacher','title','detail','student_status','add_time']
    
    def __init__(self, *args, **kwargs):
        super(StudentTrainingAssignmentSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields  = ['student','teacher','notif_subject','notif_for','notif_status','notif_time']
        
class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Training
        fields  = ['id','title','slug','description','overview','category','thumbnail','duration','price','teacher','training_chapter','related_training','total_training_enrolled','add_time']
    
    def __init__(self, *args, **kwargs):
        super(TrainingSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

        
class TrainingChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrainingChapter
        fields  = ['id','training','title','slug','description','video','add_time']
        
class StudentTrainingEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentTrainingEnrollment
        fields  = ['training','student','enrolled_time']
        
    def __init__(self, *args, **kwargs):
        super(StudentTrainingEnrollSerializer,self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            
class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = models.Order
        fields = '__all__'
        depth = 2