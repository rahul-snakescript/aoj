from django.conf.urls import url
from django.views.generic import RedirectView

from .views import DashOrdersView, DashProfileView, DashPasswordChangeView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name="dashboard:orders"), name='index'),
    url(r'^orders/$', DashOrdersView.as_view(), name='orders'),
    url(r'^profile/$', DashProfileView.as_view(), name='profile'),
    url(r'^password/$', DashPasswordChangeView.as_view(), name='password'),
]
