from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard/$', views.dashboard),
    url(r'^createuser/$', views.createUser),
    url(r'^trips/new/$', views.addtrip),
    url(r'^logout/$', views.logout),
    url(r'^addtrip/$', views.addtrip),
    url(r'^trips/join/(?P<trip_id>\d+)/$', views.tripjoin),
    url(r'^trips/edit/(?P<trip_id>\d+)/$', views.edittrip),
    url(r'^trips/cancel/(?P<trip_id>\d+)/$', views.tripcancel),
    url(r'^createtrip/$', views.createtrip),
    url(r'^validate_login/$', views.validate_login),
    url(r'^validate_trip/$', views.validate_trip),
    url(r'^trips/(?P<trip_id>\d+)/$', views.tripview),
  url(r'^deletetrip/(?P<trip_id>\d+)/$', views.deletetrip),

]