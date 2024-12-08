from django.db import models
from django.core import serializers
from django.utils import timezone
from django.utils.text import slugify
import random
from django.core.mail import send_mail


# Create your models here.


class roles(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "9. Roles"
        
    def __str__(self):
        return self.name

#Teacher Model
class Teacher(models.Model):
    profile_img = models.ImageField(upload_to='instructor_profile_img/', null=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    verify_status =models.BooleanField(default=False)
    otp_digit = models.CharField(max_length=10,null=True)
    login_via_otp =models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural= "1. Teacher"
        
    def total_teacher_cource(self):
        total_cource=Cource.objects.filter(teacher=self).count()
        total_training=Training.objects.filter(teacher=self).count()
        return total_cource + total_training
    
    def total_teacher_chapter(self):
        total_chapter=Chapter.objects.filter(cource__teacher=self).count()
        total_training_chapter=TrainingChapter.objects.filter(training__teacher=self).count()
        return total_chapter+total_training_chapter
    
    def total_teacher_student(self):
        total_student=StudentCourceEnrollment.objects.filter(cource__teacher=self).count()
        total_training_student=StudentTrainingEnrollment.objects.filter(training__teacher=self).count()
        return total_student+total_training_student
    
  
#cource category Model  
class CourceCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural= "4. Cource Categories"
        
    def __str__(self):
        return self.title
    
#cource Model  
class Cource(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True,null=True)
    description = models.TextField(null=True)
    overview = models.TextField(null=True)
    category = models.ForeignKey(CourceCategory, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='internship_thumbnail/', null=True)
    requirement = models.TextField(null=True)
    duration =  models.IntegerField( null=True)
    price = models.IntegerField( null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_cource')
    add_time = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(Cource, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural= "3. Cource"
    
    def __str__(self):
        return self.title
    
    def total_enrolled(self):
        total_enrolled = StudentCourceEnrollment.objects.filter(cource=self).count()
        return total_enrolled
    
    def related_Cource(self):
        relatedCource = Cource.objects.filter(category_id=self.category)
        return serializers.serialize('json',relatedCource)
    
#videos model 
class Chapter(models.Model):
    cource = models.ForeignKey(Cource, on_delete=models.CASCADE, related_name='cource_chapter')
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True,null=True)
    description = models.TextField(null=True)
    video = models.FileField(upload_to='internship_videos/', )
    # duration =  models.IntegerField( null=True)
    add_time = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(Chapter, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural= "5. Videos"
    
    def __str__(self):
        return self.title
    
#student detail model 

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    dob = models.DateField(null=True)
    college = models.CharField(max_length=200,null=True)
    year= models.CharField(null=True, max_length=20)
    department= models.CharField(null=True, max_length=50)
    state = models.CharField(null=True, max_length=100)
    city= models.CharField(null=True, max_length=100)
    domain= models.CharField(null=True, max_length=20)
    refer_code= models.CharField(null=True, max_length=20)
    verify_status =models.BooleanField(default=False)
    otp_digit = models.CharField(max_length=10,null=True)
    login_via_otp =models.BooleanField(default=True)
    registration_date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.otp_digit == 0:
                self.otp_digit = random.randint(1000,9999)
            if self.email:
                send_mail(
                'Registration Successful',
                'Registration Successful',
                'shashwat.allswift@gmail.com',
                [self.email],
                fail_silently=False,
                html_message=f"""<div>
                                <div>
                                    <h1>Welcome to Allswift Solutions!</h1>
                                </div>
                                <div>
                                    <p>Dear <strong>{self.full_name}</strong>,</p>
                                    <p>Welcome to the Allswift Solutions family! We’re thrilled to have you onboard. 🎉</p>
                                    <p>
                                        At Allswift Solutions, we are dedicated to providing 
                                        <strong>innovative business solutions tailored to your needs</strong>. 
                                        As a valued member, you now have access to a range of tools, resources, and exceptional support designed to help you achieve your goals.
                                    </p>
                                    <p>Here’s how you can get started:</p>
                                    <ol>
                                        <li>Log in to your account here: <a href='http://localhost:5173/login'>Login Now</a>.</li>
                                        <li>Explore our resources and tools to get the most out of your experience.</li>
                                        <li>Contact us anytime if you have questions or need assistance.</li>
                                    </ol>
                                    <a href='http://localhost:5173/dashboard/'>Go to Dashboard</a>
                                    <p>
                                        Our support team is here for you every step of the way. You can reach us at 
                                        <a href='mailto:allswiftsolutions@gmail.com'>allswiftsolutions@gmail.com</a> or call us at +91 9315484147.
                                    </p>
                                    <p>
                                        Once again, thank you for choosing Allswift Solutions. We look forward to working with you and seeing you succeed!
                                    </p>
                                </div>
                                <div >
                                    <p>Warm regards,</p>
                                    <p>
                                        <a href='http://localhost:5173/'>Allswift Solutions</a>
                                    </p>
                                </div>
                                </div>"""
            )    
            super(Student, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural= "2. Students"
    
    def __str__(self):
        return self.full_name

class ReferCode(models.Model):
    code = models.IntegerField(unique=True, blank=True,null=True)
    hr_name = models.CharField(max_length=20,null=True)
    def save(self, *args, **kwargs):
            if not self.code:
                self.code = random.randint(100000,999999)
            super(ReferCode, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural= "16. Refer Code"
    
    def __str__(self):
        return f'{self.hr_name} - {self.code}'
    
    
#Enrollment info 
class StudentCourceEnrollment(models.Model):
    cource = models.ForeignKey(Cource, on_delete=models.CASCADE, related_name='enrolled_cource')
    student  =  models.ForeignKey(Student,on_delete=models.CASCADE, related_name='enrolled_student')
    enrolled_time= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural= "6. Student Cource Enrollment"
    
    def __str__(self):
        return f'{self.cource}-{self.student}'
#add to favorite info
class FavoriteCource(models.Model):
    cource = models.ForeignKey(Cource,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural= "7. Student Favorite Cource"
    
    def __str__(self):
        return f'{self.cource}-{self.student}'

class BlogCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural= "12. Blog Categories"
        
    def __str__(self):
        return self.title
    
class blog(models.Model):
    title = models.CharField(max_length=150, primary_key=True)
    slug = models.SlugField(unique=True, blank=True,null=True)
    desc = models.CharField(max_length=100,null=True)
    update_time= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Teacher,on_delete=models.CASCADE)  # example field
    img1 = models.ImageField(upload_to='blog_images/', null=True)
    article1 = models.TextField(null=True)
    img2 = models.ImageField(upload_to='blog_images/', null=True)
    article2 = models.TextField(null=True)
    category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE, null=True)  # example field
    
    def save(self, *args, **kwargs):
            # Automatically generate a slug from the title if it's not provided
            if not self.slug:
                self.slug = slugify(self.title)
            super(blog, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "8. Blog"
        
    def __str__(self):
        return self.title
    

    
class Assignments(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    title = models.CharField(max_length=150, primary_key=True)
    detail = models.TextField(null=True)
    student_status = models.BooleanField(default=False, null=True)
    add_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "10. Assignments"
        
        
    def __str__(self):
        return self.title

class Notification(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, verbose_name='student')
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='teacher')
    notif_subject=models.CharField(max_length=200,verbose_name='subject')
    notif_for=models.CharField(max_length=200,verbose_name='detail')
    notif_status = models.BooleanField(default=False,verbose_name='Status')
    notif_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "11. Notification"
    def __str__(self):
        return self.notif_subject


#Training Model  
class Training(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True,null=True)
    description = models.TextField(null=True)
    overview = models.TextField(null=True)
    category = models.ForeignKey(CourceCategory, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='training_thumbnail/', null=True)
    duration =  models.IntegerField( null=True)
    price = models.IntegerField( null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_training')
    add_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural= "13. Training"
    
    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(Training, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def total_training_enrolled(self):
        total_training_enrolled = StudentTrainingEnrollment.objects.filter(training=self).count()
        return total_training_enrolled
    
    def related_training(self):
        relatedTraining = Training.objects.filter(category_id=self.category)
        return serializers.serialize('json',relatedTraining)
    
class StudentTrainingEnrollment(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='enrolled_training')
    student  =  models.ForeignKey(Student,on_delete=models.CASCADE, related_name='enrolled_training_student')
    enrolled_time= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural= "14. Student Training Enrollment"
    
    def __str__(self):
        return f'{self.training}-{self.student}'
    
class TrainingChapter(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='training_chapter')
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True,null=True)
    description = models.TextField(null=True)
    video = models.FileField(upload_to='training_videos/')
    # duration =  models.IntegerField(null=True)
    add_time = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(TrainingChapter, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural= "15. Training Videos"  
    
    def __str__(self):
        return self.title

class TrainingAssignments(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    title = models.CharField(max_length=150, primary_key=True)
    detail = models.TextField(null=True)
    student_status = models.BooleanField(default=False, null=True)
    add_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "10. Training Assignments"
        
        
    def __str__(self):
        return self.title
    
    
class Order(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    order_product = models.ForeignKey(Cource, on_delete= models.CASCADE, null=True)
    order_id = models.IntegerField(null=True, blank=True)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if it's not provided
        if not self.order_id:
            self.order_id = random.randint(100000,999999)
        super(Order, self).save(*args, **kwargs)
        if self.user.email:
            send_mail(
                'Enrollment Successful',
                'Please Verify Your Account',
                'allswiftsolutions@gmail.com',
                [self.user.email],
                fail_silently=False,
                html_message=f"""
                    <h1>Payment Successful</h1>
                    <p>Your are now enrolled in {self.order_product.title} program</p>
                    <p>Click the button below to downlaod invoice: </p>
                    <a href="http://127.0.0.1:8000/api/invoice/{self.order_id}/"><button>Download Invoice</button></a>
                    <p>Thank you.</p>
                """
            )
        
        
    class Meta:
        verbose_name_plural = "17. Orders"
        
    def __str__(self):
        return self.order_product.title