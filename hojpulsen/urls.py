from django.contrib import admin
from django.urls import path
from train import views

urlpatterns = [
	path('', views.startpage),
	path('slideshow', views.slideshow),
    path('admin/', admin.site.urls),
]
