from pyexpat import model
from statistics import mode

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import datetime

from django.utils import timezone

from .settings import PERIOD,PIC_URL,PIC_HIS_URL

# Create your models here.

DEGREE_CHOICES = (
    (u'本科', u'本科'),
    (u'硕士', u'硕士'),
    (u'博士', u'博士'),
)

class Candidate(models.Model):
    num = models.PositiveIntegerField(u'大众投票数', default=0)
    name = models.CharField(u'名字', max_length=100)
    show_num = models.IntegerField(u'编号', default=0, unique=True)
    college = models.CharField(u'院系', max_length=100, blank=True, null=True)
    degree = models.CharField(u'学位', max_length=15, choices=DEGREE_CHOICES, default='under')
    grade = models.CharField(u'年级', max_length=20, blank=True, null=True)
    photo = models.CharField(u'照片文件名', max_length=500, default=u'example.jpg')
    statement = models.CharField(u'宣言', max_length=150)
    intro = models.CharField(u'主要事迹',max_length=1000)
    record = models.CharField(u'每天得票数', max_length=1000, default='0' + (',0' * (PERIOD - 1)))
    expert_num = models.PositiveIntegerField(u'专家投票数', default=0)
    leader_num = models.PositiveIntegerField(u'学生代表投票数', default=0)
    def __str__(self):
        return self.name

    def GetPicPath(self):
        return PIC_URL+str(self.show_num)+'/'

class Member(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date = models.DateField(default='1000-01-01', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Expert(models.Model):
    whuid = models.CharField(max_length=13)

    def __str__(self):
        return self.id

class Leader(models.Model):
    whuid = models.CharField(max_length=13)

    def __str__(self):
        return self.id

class IP(models.Model):
    ip = models.GenericIPAddressField()
    num = models.PositiveIntegerField(u'今日投票数', default=0)
    total = models.PositiveIntegerField(u'本阶段投票数', default=0)
    date = models.DateField(default='1000-01-01')

    def __str__(self):
        return "%s" % self.ip

class Announcement(models.Model):
    info = models.TextField(max_length=1000)

class Device(models.Model):
    uuid = models.CharField(max_length=200)
    ua = models.CharField(u'User Agent',max_length=200)
    finger_print = models.CharField(u'浏览器指纹',max_length=200)
    num = models.PositiveIntegerField(u'今日投票数', default=0)
    total = models.PositiveIntegerField(u'本阶段投票数', default=0)
    date = models.DateField(default='1000-01-01')

    def __str__(self):
        return "%s" % self.uuid

class Voter(models.Model):
    ip = models.ForeignKey(IP,on_delete=models.CASCADE,blank=True)
    device = models.ForeignKey(Device,on_delete=models.CASCADE,blank=True)
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    ua = models.CharField(u'User Agent', max_length=200,blank=True)
    finger_print = models.CharField(u'浏览器指纹', max_length=200,blank=True)
    candidates = models.ManyToManyField(Candidate, blank=True)
    time = models.DateTimeField(auto_now_add=True)

class IllegalVote(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    reason = models.CharField(u'错误理由', max_length=200)
    tag = models.IntegerField(u'错误标签')
    candidates = models.ManyToManyField(Candidate, blank=True)
    time = models.DateTimeField(auto_now_add=True)

YEAR_CHOICES =[(i,i) for i in range(2006,datetime.date.today().year,1)]

class History(models.Model):

    name = models.CharField(u'名字', max_length=100)
    show_num = models.IntegerField(u'编号', default=0)
    college = models.CharField(u'院系', max_length=100, blank=True, null=True)
    degree = models.CharField(u'学位', max_length=15, choices=DEGREE_CHOICES, default='under',blank=True,null=True)
    grade = models.CharField(u'年级', max_length=20, blank=True, null=True)
    photo = models.CharField(u'照片文件名', max_length=500, default=u'example.jpg')
    statement = models.CharField(u'宣言', max_length=150,blank=True, null=True)
    intro = models.CharField(u'主要事迹',max_length=1000,blank=True, null=True)
    years = models.IntegerField(u'参选年份', choices=YEAR_CHOICES)

    def GetPicPath(self):
        return PIC_HIS_URL+str(self.show_num)+'/'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    