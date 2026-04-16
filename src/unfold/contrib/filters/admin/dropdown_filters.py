from collections.abc import Iterator
from typing import Any

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import Field, Model, QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from unfold.contrib.filters.admin.mixins import (
    DropdownMixin,
    MultiValueMixin,
    ValueMixin,
)
from unfold.contrib.filters.forms import DropdownForm


class DropdownFilter(admin.SimpleListFilter):
    template = "unfold/filters/filters_field.html"
    form_class = DropdownForm
    all_option = ["", _("All")]

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class MultipleDropdownFilter(DropdownFilter):
    multiple = True
    used_parameters: dict[str, list[str]]

    def __init__(
        self,
        request: HttpRequest,
        params: dict[str, Any],
        model: type[Model],
        model_admin: ModelAdmin,
    ) -> None:
        self.request = request
        super().__init__(request, params, model, model_admin)

        if (
            self.parameter_name is not None
            and isinstance(self.parameter_name, str)
            and self.parameter_name in self.request.GET
        ):
            self.used_parameters[self.parameter_name] = self.request.GET.getlist(
                self.parameter_name
            )


class ChoicesDropdownFilter(ValueMixin, DropdownMixin, admin.ChoicesFieldListFilter):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class MultipleChoicesDropdownFilter(MultiValueMixin, ChoicesDropdownFilter):
    multiple = True


class RelatedDropdownFilter(ValueMixin, DropdownMixin, admin.RelatedFieldListFilter):
    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        super().__init__(field, request, params, model, model_admin, field_path)
        self.model_admin = model_admin
        self.request = request

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class MultipleRelatedDropdownFilter(MultiValueMixin, RelatedDropdownFilter):
    multiple = True
