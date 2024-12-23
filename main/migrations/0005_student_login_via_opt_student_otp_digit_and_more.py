# Generated by Django 4.2.3 on 2024-10-31 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_chapter_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='login_via_opt',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='otp_digit',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='verify_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teacher',
            name='login_via_opt',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teacher',
            name='otp_digit',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='verify_status',
            field=models.BooleanField(default=False),
        ),
    ]
