from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.home), 
    url(r'^login$', views.login), 
    url(r'^registration$', views.registration),
    url(r'^books/add$', views.add), 
    url(r'^processadd$', views.processadd), 
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^books/(?P<id>\d+)$', views.showbook), 
    url(r'^addreview/(?P<id>\d+)$', views.addreview),
    url(r'^deletereview/(?P<id>\d+)$', views.deletereview),
]