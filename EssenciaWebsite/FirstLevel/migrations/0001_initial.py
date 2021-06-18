# Generated by Django 3.2.3 on 2021-06-14 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='loginpage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30)),
                ('Emp_ID', models.CharField(blank=True, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('confirm_password', models.CharField(max_length=30)),
                ('confirm_email', models.EmailField(max_length=254, unique=True)),
                ('First_Name', models.CharField(max_length=30)),
                ('Last_Name', models.CharField(max_length=30)),
                ('Emp_ID', models.CharField(max_length=6, unique=True)),
            ],
        ),
    ]