from dataclasses import fields
from pyexpat import model
from rest_framework.serializers import ModelSerializer,CharField
from .models import Candidate,History,Announcement
class CandidateSerializer(ModelSerializer):
    
    photo = CharField(max_length=500, source = 'GetPicPath')

    class Meta:
        model = Candidate
        exclude = ('id',)

class HistorySerializer(ModelSerializer):
    photo = CharField(max_length=500, source = 'GetPicPath')

    class Meta:
        model = History
        exclude = ('id',)

class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = Announcement
        exclude = ('id',)
