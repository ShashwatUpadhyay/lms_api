# Generated by Django 4.2.3 on 2024-11-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_order_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
