from django.urls import path
from .import views

urlpatterns = [
    path('', views.blogPosts, name="blog"),
    path('<str:id>/<slug:slug>', views.blogDetails, name="blog_details"),
    path('search/', views.search, name='search'),
    path('category/<str:id>/<slug:slug>/', views.categoryView, name="category"),
    path('tag/<str:id>/<slug:slug>/', views.taggedView, name="tagged"),
]
