from django.urls import re_path,include
from . import views

urlpatterns = [
    re_path('^vote/$',views.VoteView.as_view()),
    re_path('^candidate/$',views.CandidateView.as_view({'get':'list'})),
    re_path('^candidate/(?P<id>\d+)/$',views.CandidateView.as_view({'get':'retrieve'})),
    re_path('^announcement/$',views.AnnoncementsView.as_view({'get':'list'})),
    re_path('^import/$',views.ImportView.as_view()),
    re_path('^photo/(?P<id>\d+)/$',views.PhotoView.as_view()),
    re_path('^historyphoto/(?P<id>\d+)/$',views.HistoryPhotoView.as_view()),
    re_path('^history/$',views.HistoryView.as_view()),
    re_path('^votestatus/$',views.VotestatusView.as_view()),
    re_path('^captcha/$',views.CaptchaView.as_view()),
    re_path('',views.IndexView.as_view())
]
