from django.urls import path,include
from . import views

urlpatterns = [
    path('^vote/(?P<id>\d+)/$',views.VoteView.as_view()),
    path('^Candidate/$',views.CandidateView.as_view({'get':'list'})),
    path('^Candidate/(?P<pk>\d+)/$',views.CandidateView.as_view({'get':'retrieve'})),
    path('^Annoncements/$',views.AnnoncementsView.as_view({'get':'list'})),
    path('^import/$',views.ImportView.as_view()),
    path('^Photo/(?P<id>\d+)/$',views.PhotoView.as_view()),
    path('^Photo/(?P<id>\d+)/$',views.HistoryPhotoView.as_view()),
    path('^HistoryView/$',views.HistoryView.as_view()),
    path('^Votestatus/$',views.VotestatusView.as_view())
]
