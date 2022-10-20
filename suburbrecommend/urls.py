"""suburbrecommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view
# from django.views.generic import TemplateView

from contactpage.views import contactpage_view
from helppage.views import helppage_view
from searchingpage.views import searchingpage, detail_view, resultpage_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', searchingpage),
    path('contactpage/', contactpage_view,),
    path('helppage/', helppage_view),
    path('resultpage/', resultpage_view),
    path('detail/<str:suburb_name_postcode>/', detail_view, name="detail")
    ]