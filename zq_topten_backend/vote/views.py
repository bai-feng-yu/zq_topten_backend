import code
from curses import noecho
from dis import show_code
import imp
import random
from msilib.schema import Error
import uuid
import xlrd
import re
from datetime import date
from re import T
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from .settings import BASE_DIR #TODO 需要进一步修改路径信息
from rest_framework.response import Response
from .ReturnMsg import ReturnMsg
from .models import Announcement, Device, IllegalVote, Member,Candidate,History
from .settings import PIC_PATH,PIC_HIS_PATH,START_DATE,END_DATE,VOTE_MIN,VOTE_MAX,IP_whiteList
from .Paginations import GeneralPagination
from .Serializer import HistorySerializer,CandidateSerializer,AnnouncementSerializer
from .Permission import VotePermission
from .Vote import IPLimitJudge,DeviceLimitJudge,StuLimitJudge,Vote,IllegalVoteRecord
# Create your views here.

class VoteView(APIView):
    permission_classes = [VotePermission]
    def post(self,request,*args,**kwargs):
        pass
        # TODO 验证码模块
        # TODO 检查指纹
        IllegalVoteTag = 0
        IllegalVoteMsg = []
        FingerPrint = request.POST.get("fingerPrint", None)
        if FingerPrint == None:
            IllegalVoteTag += 64
            IllegalVoteMsg.append('获取浏览器指纹失败')
        # TODO 检查日期
        if not START_DATE <= date.today() <= END_DATE:
            return Response(ReturnMsg(Code = 302,Msg='本阶段投票已经结束').Data)
        # TODO 检查IP
        IPAddress = request.META.get('REMOTE_ADDR', None)
        if IPAddress == None:
            return Response(ReturnMsg(Code = 303,Msg='IP获取失败').Data)

        # 地理位置限制IP访问（如只能武汉IP访问），在移动网络情况下误杀率过高

        # TODO 获取客户端信息

        uuid = request.COOKIES.get('uuid',None)
        ua = request.META.get('HTTP_USER_AGENT',None)
        if uuid == None or ua == None:
            return Response(ReturnMsg(Code = 304,Msg='投票异常，请检查浏览器COOKIES是否开启').Data)
        uuid_regex = re.compile(r"[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}")
        if not uuid_regex.match(uuid):
            return Response(ReturnMsg(Code = 304,Msg='投票异常，请检查浏览器COOKIES是否开启').Data)
        
        # TODO 获取投票人
        try:
            candidates = request.POST.getlist('id[]')
        except:
            return Response(ReturnMsg(Code = 305,Msg='缺少投票数据' % VOTE_MIN).Data)
        candidates = list(set(candidates)) # 防止list中有相同ID
        CandidatesList = []
        if len(candidates) < VOTE_MIN:
            return Response(ReturnMsg(Code = 300,Msg='投票人数不能低于%d人' % VOTE_MIN).Data)
        if len(candidates) > VOTE_MAX:
            return Response(ReturnMsg(Code = 301,Msg='投票人数不能高于%d人' % VOTE_MAX).Data)
        
        for candidate in candidates: # TODO show_num 和 id的关系?
            try:
                candy = Candidate.objects.get(show_num = candidate)
                CandidatesList.append(candy)
            except Candidate.DoesNotExist:
                return Response(ReturnMsg(Code = 306,Msg='投票数据错误' % VOTE_MAX).Data)
        # TODO 判断IP投票限制

        IPJudgeResult = IPLimitJudge(IPAddress)
        if IPJudgeResult[0] != 0:
            IllegalVoteTag += IPJudgeResult[0]
            IllegalVoteMsg.append(*IPJudgeResult[1])

        # TODO 判断用户投票限制
        
        DeviceJudgeResult = DeviceLimitJudge(uuid,ua,FingerPrint)
        if DeviceJudgeResult[0] != 0:
            IllegalVoteTag += DeviceJudgeResult[0]
            IllegalVoteMsg.append(*DeviceJudgeResult[1])
        
        StuJudgeResult = StuLimitJudge(request.Stu)
        if StuJudgeResult[0] != 0:
            IllegalVoteTag += StuJudgeResult[0]
            IllegalVoteMsg.append(*StuJudgeResult[1])
        
        # TODO 投票过程
        if IllegalVoteTag == 0:
            Vote(IPJudgeResult[2],DeviceJudgeResult[2],StuJudgeResult[2],ua,FingerPrint,CandidatesList)
            rank = Candidate.objects.order_by('-num')
            ser = CandidateSerializer(instance=Candidate,many=True)
            Ret = ser.data
            _rank = 0
            for ret in Ret:
                _rank += 1
                ret.update('rank',_rank)
            return Response(ReturnMsg(Code = 200,Msg='投票成功',Data=Ret).Data)
        else:
            IllegalVoteRecord(IPJudgeResult[2],DeviceJudgeResult[2],StuJudgeResult[2],ua,FingerPrint,CandidatesList,IllegalVoteTag,IllegalVoteMsg)
            return Response(ReturnMsg(Code = 307,Msg='投票过程出现异常').Data)

class VotestatusView(APIView):
    def get(self,request,*args,**kwargs):
        if START_DATE <= date.today() <= END_DATE:
            isVoteAvaliable = 1
            return Response(ReturnMsg(Code=200,Msg='获取成功',isVoteAvaliable = 1,detail = '允许投票').Data)
        else:
            isVoteAvaliable = 0
            return Response(ReturnMsg(Code=200,Msg='获取成功',isVoteAvaliable = 0,detail = '投票过期').Data)

class CandidateView(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = GeneralPagination
    def list(self,request,*args,**kwargs):
        # TODO 随机排列
        res = super().list(request,args,kwargs)
        random.shuffle(res.data)
        return Response(ReturnMsg(Code=200,Msg='获取成功',Data=res).Data)
    def retrieve(self, request, *args, **kwargs):
        try:
            res = super().retrieve(request, *args, **kwargs)
            return Response(ReturnMsg(Code=200,Msg='获取成功',Data=res).Data)
        except Http404:
            return Response(ReturnMsg(Code=400,Msg='不存在该候选人').Data)

class AnnoncementsView(ListModelMixin,GenericViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    pagination_class = GeneralPagination
    def list(self,request,*args,**kwargs):
        res = super().list(request,args,kwargs)
        return Response(ReturnMsg(Code=200,Msg='获取成功',Data=res).Data)

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
            candidate = Candidate.objects.get(show_num = id)
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
        