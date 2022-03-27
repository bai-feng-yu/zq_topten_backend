import imp
import xlrd
from re import T
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from .settings import BASE_DIR #TODO 需要进一步修改路径信息
from rest_framework.response import Response
from .ReturnMsg import ReturnMsg
from .models import Announcement, Member,Candidate,History
from .settings import PIC_PATH,PIC_HIS_PATH
from .Paginations import GeneralPagination
from .Serializer import HistorySerializer,CandidateSerializer,AnnouncementSerializer
from .Permission import VotePermission
# Create your views here.

class VoteView(APIView):
    permission_classes = [VotePermission]
    def post(self,request,*args,**kwargs):
        pass
        # TODO 验证码模块
        # TODO 检查指纹
        # TODO 检查日期
        # TODO 检查IP
        # TODO 获取客户端信息

        # TODO 获取投票人

        # TODO 判断IP投票限制
        # TODO 判断用户投票限制
        
        # TODO 投票过程


class CandidateView(ListModelMixin,RetrieveModelMixin,GenericViewSet): # TODO 日期检查
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = GeneralPagination

class AnnoncementsView(ListModelMixin,GenericViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    pagination_class = GeneralPagination

class ImportView(APIView):
    def get(self,request,*args,**kwargs):
        xls_path = BASE_DIR + r'/stu_auth.xlsx'  # 数据量超过65535行，只能存储为xlsx格式，且2017年11月后xlrd直接支持xlsx格式，无需指定文件类型
        data = xlrd.open_workbook(xls_path)
        xs_sheet = data.sheet_by_name('stu_auth')
        try:
            for i in range(0, xs_sheet.nrows):
                a = xs_sheet.cell(i, 0)
                b = xs_sheet.cell(i, 1)
                bstr = str(b.value)
                bstr = bstr[bstr.__len__()-7:bstr.__len__()-1]
                a = str(a.value)
                if len(a) != 13:
                    continue
                try:
                    member = Member.objects.get(student_id=a)
                    member.password = bstr
                except Member.DoesNotExist:
                    member = Member(student_id=a, password=bstr)
                member.save()
                return Response(ReturnMsg(200,'导入成功').Data)
        except:
            return Response(ReturnMsg(300,'导入失败').Data)

class BasePhotoView(APIView):
    BasePath = ''
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id',None)
        if not id:
            return Response(ReturnMsg(301,'缺少ID参数').Data)
        try:
            candidate = Candidate.objects.get(id = id)
        except Candidate.DoesNotExist:
            return Response(ReturnMsg(302,'不存在该ID').Data)
        name = candidate.photo
        path = self.BasePath+name
        with open(path,'rb') as f: #TODO 测试图片不存在
            data = f.read()
        return HttpResponse(data)

class PhotoView(BasePhotoView):
    BathPath = PIC_PATH

class HistoryPhotoView(BasePhotoView):
    BathPath = PIC_HIS_PATH

class HistoryView(APIView):
    def get(self,request,*args,**kwargs):
        queryset = History.objects.all()
        paginator = GeneralPagination()
        pg_history = paginator.paginate_queryset(queryset=queryset,request=request,view=self)
        history_ser = HistorySerializer(instance=pg_history,many = True)
        return Response(ReturnMsg(200,'获取成功',[paginator.get_paginated_response(history_ser.data)]))
        