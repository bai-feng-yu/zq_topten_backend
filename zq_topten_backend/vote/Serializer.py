from dataclasses import fields
from pyexpat import model
from rest_framework.serializers import ModelSerializer,CharField
from .models import Candidate,History,Announcement
class CandidateSerializer(ModelSerializer):
    
    photo = CharField(max_length=500, source = 'GetPicPath')

    class Meta:
        model = Candidate
        fields = '__all__'

class HistorySerializer(ModelSerializer):
    photo = CharField(max_length=500, source = 'GetPicPath')

    class Meta:
        model = History
        fields = '__all__'

class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
