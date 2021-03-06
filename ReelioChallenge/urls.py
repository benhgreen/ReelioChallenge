"""ReelioChallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from TodoAPI import views
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'lists', views.TodoListViewSet, base_name='lists')
router.register(r'items', views.TodoItemViewSet, base_name='items')
router.register(r'users', views.UserViewSet, base_name='users')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^register', views.create_user, name='register_user'),
    url(r'^recover/([0-9]+)', views.restore_item, name='restore')
]
