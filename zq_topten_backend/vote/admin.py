from django.contrib import admin
from vote.models import Candidate, Member, IP, Voter, Announcement, Device, IllegalVote, History
from django.shortcuts import HttpResponse

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('show_num', 'name', 'num', 'grade', 'id', 'photo', 'record')
    ordering = ('show_num',)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'password', 'date')


class VoterAdmin(admin.ModelAdmin):
    list_display = ('member', 'ip', 'time', 'finger_print')


class IPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'num', 'total', 'date')


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('info',)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'ua', 'date', 'finger_print')


class IllegalVoteAdmin(admin.ModelAdmin):
    list_display = ('member', 'device', 'tag', 'time')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('show_num', 'name' , 'grade', 'id', 'years','photo')
    ordering = ('show_num',)


admin.site.register(History, HistoryAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Member)
admin.site.register(IP, IPAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(IllegalVote, IllegalVoteAdmin)