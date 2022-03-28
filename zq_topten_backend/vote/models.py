from pyexpat import model
from statistics import mode
from django.db import models
import datetime
from .settings import PERIOD,PIC_URL,PIC_HIS_URL

# Create your models here.

DEGREE_CHOICES = (
    (u'本科', u'本科'),
    (u'硕士', u'硕士'),
    (u'博士', u'博士'),
)

class Candidate(models.Model):
    num = models.PositiveIntegerField(u'投票数', default=0)
    name = models.CharField(u'名字', max_length=100)
    show_num = models.IntegerField(u'编号', default=0)
    college = models.CharField(u'院系', max_length=100, blank=True, null=True)
    degree = models.CharField(u'学位', max_length=15, choices=DEGREE_CHOICES, default='under')
    grade = models.CharField(u'年级', max_length=20, blank=True, null=True)
    photo = models.CharField(u'照片文件名', max_length=500, default=u'example.jpg')
    statement = models.CharField(u'宣言', max_length=150)
    intro = models.CharField(u'主要事迹',max_length=1000)
    record = models.CharField(u'每天得票数', max_length=1000, default='0' + (',0' * (PERIOD - 1)))

    def GetPicPath(self):
        return PIC_URL+str(self.show_num)+'/'

class Member(models.Model):
    student_id = models.CharField(max_length=13)
    password = models.CharField(max_length=6)
    date = models.DateField(default='1000-01-01', null=True, blank=True)

    def __str__(self):
        return self.student_id

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
    ip = models.ForeignKey(IP)
    device = models.ForeignKey(Device)
    member = models.ForeignKey(Member)
    ua = models.CharField(u'User Agent', max_length=200)
    finger_print = models.CharField(u'浏览器指纹', max_length=200)
    candidates = models.ManyToManyField(Candidate, blank=True)
    time = models.DateTimeField(auto_now_add=True)

class IllegalVote(models.Model):
    member = models.ForeignKey(Member)
    ip = models.ForeignKey(IP)
    device = models.ForeignKey(Device)
    reason = models.CharField(u'错误理由', max_length=200)
    tag = models.IntegerField(u'错误标签')
    ua = models.CharField(u'User Agent', max_length=200)
    finger_print = models.CharField(u'浏览器指纹', max_length=200)
    candidates = models.ManyToManyField(Candidate, blank=True)
    time = models.DateTimeField(auto_now_add=True)

YEAR_CHOICES =[(i,i) for i in range(2006,datetime.date.today().year,1)]

class History(models.Model):

    num = models.PositiveIntegerField(u'投票数', default=0)
    name = models.CharField(u'名字', max_length=100)
    show_num = models.IntegerField(u'编号', default=0)
    college = models.CharField(u'院系', max_length=100, blank=True, null=True)
    degree = models.CharField(u'学位', max_length=15, choices=DEGREE_CHOICES, default='under')
    grade = models.CharField(u'年级', max_length=20, blank=True, null=True)
    photo = models.CharField(u'照片文件名', max_length=500, default=u'example.jpg')
    statement = models.CharField(u'宣言', max_length=150)
    intro = models.CharField(u'主要事迹',max_length=1000)
    record = models.CharField(u'每天得票数', max_length=1000, default='0' + (',0' * (PERIOD - 1)))

    def GetPicPath(self):
        return PIC_HIS_URL+str(self.show_num)+'/'

    def __unicode__(self):
        return self.name
    