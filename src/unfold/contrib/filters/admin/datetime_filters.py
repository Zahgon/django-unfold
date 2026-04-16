from collections.abc import Iterator

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import Model, QuerySet
from django.db.models.fields import DateField, DateTimeField, Field
from django.forms import ValidationError
from django.http import HttpRequest

from unfold.contrib.filters.forms import RangeDateForm, RangeDateTimeForm
from unfold.utils import parse_date_str, parse_datetime_str


class RangeDateFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    form_class = RangeDateForm
    template = "unfold/filters/filters_date_range.html"

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
        if not isinstance(field, DateField):
            raise TypeError(
                f"Class {type(self.field)} is not supported for {self.__class__.__name__}."
            )

        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name + "_from" in params:
            value = params.pop(self.field_path + "_from")
            value = value[0] if isinstance(value, list) else value

            if value not in EMPTY_VALUES:
                self.used_parameters[self.field_path + "_from"] = value

        if self.parameter_name + "_to" in params:
            value = params.pop(self.field_path + "_to")
            value = value[0] if isinstance(value, list) else value

            if value not in EMPTY_VALUES:
                self.used_parameters[self.field_path + "_to"] = value

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        pass

    def expected_parameters(self) -> list[str | None]:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class RangeDateTimeFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = "unfold/filters/filters_datetime_range.html"
    form_class = RangeDateTimeForm

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
        if not isinstance(field, DateTimeField):
            raise TypeError(
                f"Class {type(self.field)} is not supported for {self.__class__.__name__}."
            )

        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name + "_from_0" in params:
            value = params.pop(self.field_path + "_from_0")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_from_0"] = value

        if self.parameter_name + "_from_1" in params:
            value = params.pop(self.field_path + "_from_1")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_from_1"] = value

        if self.parameter_name + "_to_0" in params:
            value = params.pop(self.field_path + "_to_0")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_to_0"] = value

        if self.parameter_name + "_to_1" in params:
            value = params.pop(self.field_path + "_to_1")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_to_1"] = value

    def expected_parameters(self) -> list[str | None]:
        pass

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass
