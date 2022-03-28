from django.urls import re_path,include
from . import views

urlpatterns = [
    re_path('^vote/(?P<id>\d+)/$',views.VoteView.as_view()),
    re_path('^Candidate/$',views.CandidateView.as_view({'get':'list'})),
    re_path('^Candidate/(?P<id>\d+)/$',views.CandidateView.as_view({'get':'retrieve'})),
    re_path('^Annoncements/$',views.AnnoncementsView.as_view({'get':'list'})),
    re_path('^import/$',views.ImportView.as_view()),
    re_path('^Photo/(?P<id>\d+)/$',views.PhotoView.as_view()),
    re_path('^HistoryPhoto/(?P<id>\d+)/$',views.HistoryPhotoView.as_view()),
    re_path('^History/$',views.HistoryView.as_view()),
    re_path('^Votestatus/$',views.VotestatusView.as_view()),
    re_path('',views.IndexView.as_view())
]
