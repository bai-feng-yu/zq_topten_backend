from datetime import date
from http import client
import json
from .settings import IP_whiteList, IP_NUM, IP_TOTAL, DEVICE_NUM, \
    DEVICE_TOTAL, START_DATE
from .models import IP, Device, Member, Voter, IllegalVote, Expert, Leader, Candidate
from datetime import date
from .Membertype import get_type


def IPLimitJudge(IPAddress):
    ip2num = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.replace(',', '.').split('.')[::-1])])
    white_list = False
    white_num = 0
    white_total = 0
    IPIllegalTag = 0
    IllegalMsg = []
    for ips in IP_whiteList:
        if ip2num(ips[0]) <= ip2num(IPAddress) <= ip2num(ips[1]):
            white_list = True
            white_num = ips[2]
            white_total = ips[3]
    try:
        ipAddress = IP.objects.get(ip=IPAddress)
        if ipAddress.date == date.today():  # 今日已经投过票了
            if white_list:  # 是白名单IP
                limit = (white_num, white_total)
            else:
                limit = (IP_NUM, IP_TOTAL)
            if ipAddress.num >= limit[0]:
                IllegalMsg.append('该IP本日投票已达%d次' % limit[0])
                IPIllegalTag += 1
            if ipAddress.num >= limit[1]:
                IllegalMsg.append('该IP本日投票已达%s次' % limit[1])
                IPIllegalTag += 2
        else:
            ipAddress.num = 0
            ipAddress.date = date.today()
            ipAddress.save()
    except IP.DoesNotExist:
        ipAddress = IP(ip=IPAddress, num=0, total=0)
        ipAddress.save()

    return (IPIllegalTag, ','.join(IllegalMsg), ipAddress)


def DeviceLimitJudge(uuid, ua, FingerPrint):
    DeviceIllegalTag = 0
    IllegalMsg = []
    try:
        device = Device.objects.get(uuid=uuid)
        if device.date == date.today():
            if device.num >= DEVICE_NUM:
                IllegalMsg.append('今日投票过多')
                DeviceIllegalTag += 4
            if device.total >= DEVICE_TOTAL:
                IllegalMsg.append('本阶段投票过多')
                DeviceIllegalTag += 8
        else:
            device.num = 0
            device.date = date.today()
            device.save()
        if device.ua != ua[:200]:
            DeviceIllegalTag += 16
    except Device.DoesNotExist:
        device = Device(uuid=uuid, ua=ua, finger_print=FingerPrint)
        device.save()

    return (DeviceIllegalTag, ','.join(IllegalMsg), device)


def StuLimitJudge(Stu):
    StuIllegalTag = 0
    IllegalMsg = []
    if Stu.date == date.today():
        IllegalMsg.append('本日您已进行过投票')
        StuIllegalTag += 32
    return (StuIllegalTag, ','.join(IllegalMsg), Stu)



def Vote(votemember,CandidatesList,membertype):

    votemember.date=date.today()
    votemember.save()

    voter = Voter(member=votemember)

    for item in CandidatesList:
        candidate=Candidate.objects.get(show_num=item.id)

        if membertype==1:
            candidate.leader_num+=item.count
        elif membertype==2:
            candidate.expert_num += item.count
        else:
            candidate.num += 1

            record = candidate.record.split(',')
            days = (date.today() - START_DATE).days

            if len(record) > days:
                record[days] = str(int(record[days]) + 1)
            else:
                while len(record) < days:  # FIX A BUG ?
                    record.append('0')
                record.append('1')

            candidate.record = ','.join(record)

        candidate.save()

        voter.candidates.add(candidate)

    voter.save()

# def Vote(stuid,ip, device, stu, ua, FingerPrint, candidates):
#     # 更新IP
#     ip.num += 1
#     ip.total += 1
#     ip.date = date.today()
#     ip.save()
#
#     # 更新客户端记录
#     device.num += 1
#     device.total += 1
#     device.date = date.today()
#     device.save()
#
#     # 更新学生数据
#     stu.date = date.today()
#     stu.save()
#
#     stuid=stuid.strip()
#
#     voter = Voter(ip=ip, device=device, member=stu, ua=ua, finger_print=FingerPrint)
#     voter.save()
#     for candidate in candidates:
#         record = candidate.record.split(',')
#         days = (date.today() - START_DATE).days
#
#         if len(record) > days:
#             record[days] = str(int(record[days]) + 1)
#         else:
#             while len(record) < days:  # FIX A BUG ?
#                 record.append('0')
#             record.append('1')
#
#         candidate.record = ','.join(record)
#         candidate.num += 1
#         candidate.save()
#         voter.candidates.add(candidate)
#
#     voter.save()


def IllegalVoteRecord(stu,candidates, IllegalTag, IllegalMsg):
    illegalVote = IllegalVote(member=stu,tag=IllegalTag)
    illegalVote.reason = json.dumps(IllegalMsg, ensure_ascii=False)
    illegalVote.save()
    for candidate in candidates:
        illegalVote.candidates.add(candidate)
    illegalVote.save()
