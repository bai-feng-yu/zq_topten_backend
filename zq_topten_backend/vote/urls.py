from django.urls import re_path,include
from . import views

urlpatterns = [
    re_path('^topten_api/vote/$',views.VoteView.as_view()),
    re_path('^topten_api/candidate/$',views.CandidateView.as_view({'get':'list'})),
    re_path('^topten_api/candidate/(?P<id>\d+)/$',views.CandidateView.as_view({'get':'retrieve'})),
    re_path('^topten_api/announcement/$',views.AnnoncementsView.as_view({'get':'list'})),
    re_path('^topten_api/import/$',views.ImportView.as_view()),
    re_path('^topten_api/photo/(?P<id>\d+)/$',views.PhotoView.as_view()),
    re_path('^topten_api/historyphoto/(?P<id>\d+)/$',views.HistoryPhotoView.as_view()),
    re_path('^topten_api/history/$',views.HistoryView.as_view()),
    re_path('^topten_api/votestatus/$',views.VotestatusView.as_view()),
    re_path('^topten_api/captcha/$',views.CaptchaView.as_view()),
    re_path('^topten_api/membertype/$',views.MembertypeView.as_view()),
    re_path('^topten_api/condition/$',views.ConditionView.as_view()),
    re_path('',views.IndexView.as_view()),
]
