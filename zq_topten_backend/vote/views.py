import random
import xlrd
import re
import hashlib
from datetime import date
from re import T
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .settings import BASE_DIR  # TODO 需要进一步修改路径信息
from .ReturnMsg import ReturnMsg
from .models import Announcement, Device, IllegalVote, Member, Candidate, History
from .settings import PIC_PATH, PIC_HIS_PATH, START_DATE, END_DATE, VOTE_MIN, VOTE_MAX, IP_whiteList
from .Paginations import GeneralPagination
from .Serializer import HistorySerializer, CandidateSerializer, AnnouncementSerializer
from .Permission import VotePermission
from .geetest import GeetestLib
from .Vote import IPLimitJudge, DeviceLimitJudge, StuLimitJudge, Vote, IllegalVoteRecord
from .Membertype import get_type
# Create your views here.

captcha_id = "4cc5a993124c4a16c1a1915ce4b510ab"
private_key = "4d3fc8dad159634daeb90b71d6ff1b5c"
ak = "wpwAmoUCOmmWjqrOR44QlD42"


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(ReturnMsg(Code=200, Msg='成功获取', Data=['2024珞珈十大风云学子']).Data)


class CaptchaView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = 'test'
        gt = GeetestLib(captcha_id, private_key)
        status = gt.pre_process(user_id)
        request.session[gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        return HttpResponse(response_str)

class VoteView(APIView):
    def post(self, request, *args, **kwargs):
        IllegalVoteTag=0
        IllegalVoteMsg = []

        try:
            if not request.user.is_authenticated:
                return Response(ReturnMsg(308, '查询成功，未登录').Data)
        except:
            return Response(ReturnMsg(501, '登录状态查询异常').Data)

        if not START_DATE <= date.today() <= END_DATE:
            return Response(ReturnMsg(Code=302, Msg='不在投票时间段内').Data)

        CandidatesList = []
        for item in request.data:
            CandidatesList.append({
                'id': item.get('show_num'),
                'count': item.get('count')
            })

        if len(CandidatesList) == 0:
            return Response(ReturnMsg(Code=305, Msg='缺少投票数据').Data)

        for candidate in CandidatesList:  # TODO show_num 和 id的关系?
            try:
                candy = Candidate.objects.get(show_num=candidate.id)
                CandidatesList.append(candy)
            except Candidate.DoesNotExist:
                return Response(ReturnMsg(Code=306, Msg='投票数据中有不存在的候选人',Data=candidate.id).Data)

        member_type = get_type(request.user.username)

        if member_type!=0:
            if request.user.date != '1000-01-01':
                IllegalVoteTag += 1
                IllegalVoteMsg.append('本阶段已投过票')

            if len(CandidatesList) < VOTE_MIN:
                return Response(ReturnMsg(Code=300, Msg='投票人数不能低于%d人' % VOTE_MIN).Data)
            if len(CandidatesList) > VOTE_MAX:
                return Response(ReturnMsg(Code=301, Msg='投票人数不能高于%d人' % VOTE_MAX).Data)

            sum=0
            for item in CandidatesList:
                sum+=item.count

            if sum<20:
                return Response(ReturnMsg(Code=303, Msg='投票数未达到20票').Data)
            if sum>20:
                return Response(ReturnMsg(Code=304, Msg='投票数超过20票').Data)

        else:
            StuJudgeResult = StuLimitJudge(request.user)  # 今天有没有投过票
            if StuJudgeResult[0] != 0:
                IllegalVoteTag += StuJudgeResult[0]
                IllegalVoteMsg.append(StuJudgeResult[1])

            if len(CandidatesList) < VOTE_MIN:
                return Response(ReturnMsg(Code=300, Msg='投票人数不能低于%d人' % VOTE_MIN).Data)
            if len(CandidatesList) > VOTE_MAX:
                return Response(ReturnMsg(Code=301, Msg='投票人数不能高于%d人' % VOTE_MAX).Data)

            for item in CandidatesList:
                if item.count>1:
                    return Response(ReturnMsg(Code=301, Msg='给每个候选人只能投1票').Data)

        if IllegalVoteTag == 0:
            Vote(request.user,CandidatesList,member_type)

            rank = Candidate.objects.order_by('-num')
            ser = CandidateSerializer(instance=rank, many=True)
            Ret = ser.data
            _rank = 0
            _last = -1
            _sz = 1
            for ret in Ret:
                if ret['num'] != _last:
                    _last = ret['num']
                    _rank += _sz
                    _sz = 1
                else:
                    _sz += 1
                ret.update({'rank': _rank})
            return Response(ReturnMsg(Code=200, Msg='投票成功', Data=Ret).Data)
        else:
            IllegalVoteRecord(request.user,CandidatesList, IllegalVoteTag, IllegalVoteMsg)
            return Response(ReturnMsg(Code=307, Msg='今日已投票或投票过程异常').Data)

# class VoteView(APIView):
#     authentication_classes = []
#     permission_classes = [VotePermission]
#     parser_classes = [JSONParser, FormParser, MultiPartParser]
#
#     def post(self, request, *args, **kwargs):
#         # TODO 验证码模块
#         gt = GeetestLib(captcha_id, private_key)
#         challenge = request.data.get(gt.FN_CHALLENGE, '')
#         validate = request.data.get(gt.FN_VALIDATE, '')
#         seccode = request.data.get(gt.FN_SECCODE, '')
#         status = request.session.get(gt.GT_STATUS_SESSION_KEY, None)
#         user_id = request.session.get("user_id", None)
#         if status and user_id:
#             gt_result = gt.success_validate(challenge, validate, seccode, user_id)
#         else:
#             gt_result = gt.failback_validate(challenge, validate, seccode)
#         if not gt_result:
#             return Response(ReturnMsg(Code=400, Msg='验证码无效').Data)
#
#         IllegalVoteTag = 0
#         IllegalVoteMsg = []
#         FingerPrint = request.data.get("fingerPrint", None)
#         if FingerPrint == None:
#             IllegalVoteTag += 64
#             IllegalVoteMsg.append('获取浏览器指纹失败')
#
#         if not START_DATE <= date.today() <= END_DATE:
#             return Response(ReturnMsg(Code=302, Msg='不在投票时间段内').Data)
#
#         if 'HTTP_X_FORWARDED_FOR' in request.META:  # 这样获取可能有问题
#             IPAddress = request.META['HTTP_X_FORWARDED_FOR']
#         else:
#             IPAddress = request.META.get('REMOTE_ADDR', None)
#         if IPAddress == None:
#             return Response(ReturnMsg(Code=303, Msg='IP获取失败').Data)
#
#         # 地理位置限制IP访问（如只能武汉IP访问），在移动网络情况下误杀率过高
#
#         # uuid = request.COOKIES.get('uuid',None) # 跨domain的cookie遇到一些问题
#         uuid = request.data.get('uuid', None)
#         ua = request.META.get('HTTP_USER_AGENT', None)
#         if uuid == None or ua == None:
#             return Response(ReturnMsg(Code=304, Msg='投票异常，请检查浏览器COOKIES是否开启').Data)
#         uuid_regex = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
#         if not uuid_regex.match(uuid):
#             return Response(ReturnMsg(Code=304, Msg='投票异常，请检查浏览器COOKIES是否开启').Data)
#
#         candidates = request.data.get('id', [])
#         if len(candidates) == 0:
#             return Response(ReturnMsg(Code=305, Msg='缺少投票数据').Data)
#         candidates = list(set(candidates))  # 防止list中有相同ID
#         CandidatesList = []
#         if len(candidates) < VOTE_MIN:
#             return Response(ReturnMsg(Code=300, Msg='投票人数不能低于%d人' % VOTE_MIN).Data)
#         if len(candidates) > VOTE_MAX:
#             return Response(ReturnMsg(Code=301, Msg='投票人数不能高于%d人' % VOTE_MAX).Data)
#
#         for candidate in candidates:  # TODO show_num 和 id的关系?
#             try:
#                 candy = Candidate.objects.get(show_num=candidate)
#                 CandidatesList.append(candy)
#             except Candidate.DoesNotExist:
#                 return Response(ReturnMsg(Code=306, Msg='投票数据错误').Data)
#
#         IPJudgeResult = IPLimitJudge(IPAddress)
#         if IPJudgeResult[0] != 0:
#             IllegalVoteTag += IPJudgeResult[0]
#             IllegalVoteMsg.append(IPJudgeResult[1])
#
#         DeviceJudgeResult = DeviceLimitJudge(uuid, ua, FingerPrint)
#         if DeviceJudgeResult[0] != 0:
#             IllegalVoteTag += DeviceJudgeResult[0]
#             IllegalVoteMsg.append(DeviceJudgeResult[1])
#
#         StuJudgeResult = StuLimitJudge(request.Stu)
#         if StuJudgeResult[0] != 0:
#             IllegalVoteTag += StuJudgeResult[0]
#             IllegalVoteMsg.append(StuJudgeResult[1])
#
#         if IllegalVoteTag == 0:
#             Vote(user_id,IPJudgeResult[2], DeviceJudgeResult[2], StuJudgeResult[2], ua, FingerPrint, CandidatesList)
#             rank = Candidate.objects.order_by('-num')
#             ser = CandidateSerializer(instance=rank, many=True)
#             Ret = ser.data
#             _rank = 0
#             _last = -1
#             _sz = 1
#             for ret in Ret:
#                 if ret['num'] != _last:
#                     _last = ret['num']
#                     _rank += _sz
#                     _sz = 1
#                 else:
#                     _sz += 1
#                 ret.update({'rank': _rank})
#             return Response(ReturnMsg(Code=200, Msg='投票成功', Data=Ret).Data)
#         else:
#             IllegalVoteRecord(IPJudgeResult[2], DeviceJudgeResult[2], StuJudgeResult[2], ua, FingerPrint,
#                               CandidatesList, IllegalVoteTag, IllegalVoteMsg)
#             return Response(ReturnMsg(Code=307, Msg='投票过程出现异常').Data)


class VotestatusView(APIView):
    def get(self,request,*args,**kwargs):
        if START_DATE <= date.today() <= END_DATE:
            isVoteAvaliable = 1
            return Response(ReturnMsg(Code=200,Msg='获取成功',isVoteAvaliable = 1,detail = '允许投票').Data)
        elif date.today() < START_DATE:
            isVoteAvaliable = 0
            return Response(ReturnMsg(Code=200,Msg='获取成功',isVoteAvaliable = 0,detail = '投票未开始').Data)
        else:
            isVoteAvaliable = 0
            return Response(ReturnMsg(Code=200,Msg='获取成功',isVoteAvaliable = 0,detail = '投票已结束').Data)

class CandidateView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    #    pagination_class = GeneralPagination
    lookup_url_kwarg = 'id'
    lookup_field = 'show_num'

    def list(self, request, *args, **kwargs):
        res = super().list(request, args, kwargs)
        random.shuffle(res.data)
        return Response(ReturnMsg(Code=200, Msg='获取成功', Data=res.data).Data)

    def retrieve(self, request, *args, **kwargs):
        try:
            res = super().retrieve(request, *args, **kwargs)
            return Response(ReturnMsg(Code=200, Msg='获取成功', Data=res.data).Data)
        except Http404:
            return Response(ReturnMsg(Code=400, Msg='不存在该候选人').Data)


class AnnoncementsView(ListModelMixin, GenericViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    #    pagination_class = GeneralPagination
    def list(self, request, *args, **kwargs):
        res = super().list(request, args, kwargs)
        return Response(ReturnMsg(Code=200, Msg='获取成功', Data=res.data).Data)


class ImportView(APIView):
    def get(self, request, *args, **kwargs):
        xls_path = BASE_DIR + r'stu_auth.xlsx'  # 数据量超过65535行，只能存储为xlsx格式，且2017年11月后xlrd直接支持xlsx格式，无需指定文件类型
        # UPDATE: xlrd1.2.0之后的版本不支持xlsx格式，只支持xls格式
        # 需要安装老版本的xlrd,pip install xlrd==1.2.0
        data = xlrd.open_workbook(xls_path)
        xs_sheet = data.sheet_by_name('stu_auth')
        try:
            for i in range(0, xs_sheet.nrows):
                a = xs_sheet.cell(i, 0)
                b = xs_sheet.cell(i, 1)
                bstr = str(b.value)
                bstr = bstr[bstr.__len__() - 7:bstr.__len__() - 1]
                bhash = hashlib.sha256(bstr.encode()).hexdigest()
                a = str(a.value)
                if len(a) != 13:
                    continue
                try:
                    member = Member.objects.get(student_id=a)
                    member.password = bhash
                except Member.DoesNotExist:
                    member = Member(student_id=a, password=bhash)
                member.save()
            return Response(ReturnMsg(200, '导入成功').Data)
        except:
            return Response(ReturnMsg(300, '导入失败').Data)


class BasePhotoView(APIView):
    BasePath = ''
    Model = None

    def get(self, request, *args, **kwargs):
        if self.Model == None:
            raise Exception('需要指定模型')
        id = kwargs.get('id', None)
        if not id:
            return Response(ReturnMsg(301, '缺少ID参数').Data)
        try:
            model = self.Model.objects.get(show_num=id)
        except self.Model.DoesNotExist:
            return Response(ReturnMsg(302, '不存在该ID').Data)
        name = model.photo
        path = self.BasePath + name
        try:
            with open(path, 'rb') as f:
                data = f.read()
            return HttpResponse(data, content_type='image/jpg')
        except FileNotFoundError:
            path = self.BasePath + 'example.jpg'
            with open(path, 'rb') as f:
                data = f.read()
            return HttpResponse(data, content_type='image/jpg')


class PhotoView(BasePhotoView):
    BasePath = PIC_PATH
    Model = Candidate


class HistoryPhotoView(BasePhotoView):
    BasePath = PIC_HIS_PATH
    Model = History


class HistoryView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = History.objects.all()
        #        paginator = GeneralPagination()
        #        pg_history = paginator.paginate_queryset(queryset=queryset,request=request,view=self)
        history_ser = HistorySerializer(instance=queryset, many=True)
        return Response(ReturnMsg(200, '获取成功', history_ser.data).Data)

class MembertypeView(APIView):
    def get(self, request, *args, **kwargs):
        member_type=get_type(request.user.username)
        if(member_type==1):
            return Response(ReturnMsg(200, '获取成功',1).Data)
        elif(member_type==2):
            return Response(ReturnMsg(200, '获取成功', 2).Data)
        elif(member_type==0):
            return Response(ReturnMsg(200, '获取成功', 0).Data)
        else:
            return Response(ReturnMsg(501, '获取失败', 0).Data)

class ConditionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return Response(ReturnMsg(200, '查询成功，已登录', 1).Data)
            else:
                return Response(ReturnMsg(200, '查询成功，未登录', 0).Data)
        except:
            return Response(ReturnMsg(501, '查询失败').Data)