"""
URL configuration for server project.

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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from app.views import EndpointViewSet
from app.views import MLModelViewSet
from app.views import MLModelStatusViewSet
from app.views import MLRequestViewSet
from app.views import PredictView
from app.views import BinanceAPI
from django.views.generic import TemplateView
from app.views import plotly
router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"mlmodels", MLModelViewSet, basename="mlmodels")
router.register(r"mlmodelstatuses", MLModelStatusViewSet,
                basename="mlmodelstatuses")
router.register(r"mlrequests", MLRequestViewSet, basename="mlrequests")

urlpatterns = [
    re_path(r"^api/v1/", include(router.urls)),
    re_path(r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"),
    re_path(r"^api/v1/klines$", BinanceAPI.as_view(), name="kline"),
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('plotly/', plotly, name='plotly'),
]
