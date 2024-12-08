from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Teacher)
admin.site.register(models.CourceCategory)
admin.site.register(models.Cource)
admin.site.register(models.Student)
admin.site.register(models.Chapter)
admin.site.register(models.StudentCourceEnrollment)
admin.site.register(models.FavoriteCource)
admin.site.register(models.blog)
admin.site.register(models.roles)
admin.site.register(models.Assignments)
admin.site.register(models.BlogCategory)
admin.site.register(models.Training)
admin.site.register(models.StudentTrainingEnrollment)
admin.site.register(models.TrainingChapter)
admin.site.register(models.TrainingAssignments)
admin.site.register(models.ReferCode)
admin.site.register(models.Order)

class NotificationAdmin(admin.ModelAdmin):
    list_display=['id','notif_subject','notif_for','notif_status']

admin.site.register(models.Notification,NotificationAdmin)
