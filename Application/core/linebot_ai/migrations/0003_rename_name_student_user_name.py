# Generated by Django 3.2.7 on 2021-09-25 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linebot_ai', '0002_alter_student_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='name',
            new_name='user_name',
        ),
    ]