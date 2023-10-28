"""
URL configuration for dynamic_page_builder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from dynamic_page import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('<slug:slug>/preview/', views.preview_page, name='preview_page'),
    path('<slug:slug>/render/', views.render_page, name='render_page'),
    path('<slug:slug>/build/', views.build_page, name='build_page'),
    path('create/', views.create_webpage, name='create_webpage'),
]
