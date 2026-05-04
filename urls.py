from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("api/portfolio/", views.portfolio_api, name="portfolio-api"),
    path("api/health/", views.health_api, name="health-api"),
]
