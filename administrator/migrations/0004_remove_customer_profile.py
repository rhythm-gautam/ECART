# Generated by Django 2.1.1 on 2018-11-20 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_remove_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profile',
        ),
    ]
