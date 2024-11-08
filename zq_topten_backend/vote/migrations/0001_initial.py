# Generated by Django 5.1.2 on 2024-10-30 10:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField(default=0, verbose_name='大众投票数')),
                ('name', models.CharField(max_length=100, verbose_name='名字')),
                ('show_num', models.IntegerField(default=0, unique=True, verbose_name='编号')),
                ('college', models.CharField(blank=True, max_length=100, null=True, verbose_name='院系')),
                ('degree', models.CharField(choices=[('本科', '本科'), ('硕士', '硕士'), ('博士', '博士')], default='under', max_length=15, verbose_name='学位')),
                ('grade', models.CharField(blank=True, max_length=20, null=True, verbose_name='年级')),
                ('photo', models.CharField(default='example.jpg', max_length=500, verbose_name='照片文件名')),
                ('statement', models.CharField(max_length=150, verbose_name='宣言')),
                ('intro', models.CharField(max_length=1000, verbose_name='主要事迹')),
                ('record', models.CharField(default='0,0,0,0', max_length=1000, verbose_name='每天得票数')),
                ('expert_num', models.PositiveIntegerField(default=0, verbose_name='专家投票数')),
                ('leader_num', models.PositiveIntegerField(default=0, verbose_name='学生代表投票数')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=200)),
                ('ua', models.CharField(max_length=200, verbose_name='User Agent')),
                ('finger_print', models.CharField(max_length=200, verbose_name='浏览器指纹')),
                ('num', models.PositiveIntegerField(default=0, verbose_name='今日投票数')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='本阶段投票数')),
                ('date', models.DateField(default='1000-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whuid', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名字')),
                ('show_num', models.IntegerField(default=0, verbose_name='编号')),
                ('college', models.CharField(blank=True, max_length=100, null=True, verbose_name='院系')),
                ('degree', models.CharField(blank=True, choices=[('本科', '本科'), ('硕士', '硕士'), ('博士', '博士')], default='under', max_length=15, null=True, verbose_name='学位')),
                ('grade', models.CharField(blank=True, max_length=20, null=True, verbose_name='年级')),
                ('photo', models.CharField(default='example.jpg', max_length=500, verbose_name='照片文件名')),
                ('statement', models.CharField(blank=True, max_length=150, null=True, verbose_name='宣言')),
                ('intro', models.CharField(blank=True, max_length=1000, null=True, verbose_name='主要事迹')),
                ('years', models.IntegerField(choices=[(2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], verbose_name='参选年份')),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('num', models.PositiveIntegerField(default=0, verbose_name='今日投票数')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='本阶段投票数')),
                ('date', models.DateField(default='1000-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whuid', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(blank=True, default='1000-01-01', null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IllegalVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200, verbose_name='错误理由')),
                ('tag', models.IntegerField(verbose_name='错误标签')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('candidates', models.ManyToManyField(blank=True, to='vote.candidate')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ua', models.CharField(blank=True, max_length=200, verbose_name='User Agent')),
                ('finger_print', models.CharField(blank=True, max_length=200, verbose_name='浏览器指纹')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('candidates', models.ManyToManyField(blank=True, to='vote.candidate')),
                ('device', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='vote.device')),
                ('ip', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='vote.ip')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
