# Generated by Django 4.2.3 on 2024-11-16 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.cource'),
        ),
    ]