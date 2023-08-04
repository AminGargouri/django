# from django.conf.urls import url
from django.urls import  re_path as url
from AutismAPP import views

urlpatterns=[
    url(r'^parent/$',views.parentAPI),
    url(r'^parent/([0-9]+)$',views.parentAPI),
    url(r'^enfant/$',views.enfantAPI),
    url(r'^enfant/([0-9]+)$',views.enfantAPI),
    url(r'^test/$',views.testsAutismeAPI),
    url(r'^test/([0-9]+)$',views.testsAutismeAPI),
    url(r'^predict/$',views.predictionAPI)


]