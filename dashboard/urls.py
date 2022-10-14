from django.urls import path
from django.views.generic import RedirectView

from .views import DashOrdersView, DashProfileView, DashPasswordChangeView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="dashboard:orders"), name='index'),
    path('orders/', DashOrdersView.as_view(), name='orders'),
    path('profile/', DashProfileView.as_view(), name='profile'),
    path('password/', DashPasswordChangeView.as_view(), name='password'),
]
