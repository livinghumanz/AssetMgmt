from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('UploadFile/',views.uploadFile,name='uploadFile'),
    path('testApi/',views.testApi, name="testApi"),
    path('log-asset/',views.log_checkin_out, name="log-asset"),
]