from typing import Any

from django.contrib import admin
from django.http import HttpRequest
from django.template.loader import render_to_string

from unfold.views import DatasetChangeList


class BaseDataset:
    tab = False
    title = None

    def __init__(
        self, request: HttpRequest, extra_context: dict[str, Any] | None
    ) -> None:
        self.request = request
        self.extra_context = extra_context

        self.model_admin_instance = self.model_admin(
            model=self.model, admin_site=admin.site
        )
        self.model_admin_instance.extra_context = self.extra_context

    @property
    def contents(self) -> str:
        pass

    @property
    def cl(self) -> DatasetChangeList:
        pass

    @property
    def id(self) -> str:
        pass

    @property
    def model_name(self) -> str:
        pass

    @property
    def model_verbose_name(self) -> str:
        pass
