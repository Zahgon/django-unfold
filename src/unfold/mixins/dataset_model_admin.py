from typing import Any

from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.views import main
from django.contrib.admin.views.main import IGNORED_PARAMS
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _


class DatasetModelAdminMixin:
    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict[str, Any] | None = None,
    ) -> TemplateResponse:
        pass
