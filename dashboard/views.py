# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from authtools.views import PasswordChangeView


class DashOrdersView(LoginRequiredMixin, ListView):
    template_name = "dashboard/pages/orders.html"

    def get_queryset(self):
        return self.request.user.checkoutrequest_set.all()


class DashProfileView(LoginRequiredMixin, UpdateView):
    template_name = "dashboard/pages/profile.html"
    fields = ["first_name","last_name"]
    success_url = reverse_lazy("dashboard:profile")

    def get_object(self, queryset=None):
        return self.request.user


class DashPasswordChangeView(PasswordChangeView):
    template_name = "dashboard/pages/password.html"
    success_url = reverse_lazy("dashboard:index")
