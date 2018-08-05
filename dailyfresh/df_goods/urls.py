from django.conf.urls import include, url
import views

urlpatterns=[
    url('^$',views.index),
    url('^list(\d+)_(\d+)_(\d+)/$',views.list),
    url('^(\d+)/$',views.detail),
]