from django.apps import AppConfig
from django.contrib import admin
from django.contrib.admin import sites

from unfold.sites import UnfoldAdminSite


class DefaultAppConfig(AppConfig):
    name = "unfold"
    default = True

    def ready(self):
        pass


class BasicAppConfig(AppConfig):
    name = "unfold"
