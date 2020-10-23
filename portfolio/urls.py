from django.urls import path
from .import views


urlpatterns = [
    path('', views.portfolioProject, name='portfolio'),
    path('<str:id>/<slug:slug>', views.portfolioDetails, name="portfolio_details"),
    path('category/<str:id>/<slug:slug>', views.categoryView, name="portfolio_category"),
]
