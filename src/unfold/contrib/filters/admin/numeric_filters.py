from collections.abc import Iterator
from typing import Any

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import Max, Min, Model, QuerySet
from django.db.models.fields import (
    AutoField,
    DecimalField,
    Field,
    FloatField,
    IntegerField,
)
from django.forms import ValidationError
from django.http import HttpRequest

from unfold.contrib.filters.admin.mixins import RangeNumericMixin
from unfold.contrib.filters.forms import SingleNumericForm, SliderNumericForm


class SingleNumericFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = "unfold/filters/filters_numeric_single.html"

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

        if not isinstance(field, DecimalField | IntegerField | FloatField | AutoField):
            raise TypeError(
                f"Class {type(self.field)} is not supported for {self.__class__.__name__}."
            )

        self.request = request

        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            value = value[0] if isinstance(value, list) else value

            if value not in EMPTY_VALUES:
                self.used_parameters[self.parameter_name] = value

    def queryset(
        self, request: HttpRequest, queryset: QuerySet[Any]
    ) -> QuerySet | None:
        pass

    def value(self) -> Any:
        if self.parameter_name:
            return self.used_parameters.get(self.parameter_name)

    def expected_parameters(self) -> list[str | None]:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class RangeNumericListFilter(RangeNumericMixin, admin.SimpleListFilter):
    def __init__(
        self,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
    ) -> None:
        super().__init__(request, params, model, model_admin)

        self.request = request
        self.init_used_parameters(params)

    def lookups(
        self, request: HttpRequest, model_admin: ModelAdmin
    ) -> tuple[tuple[str, str], ...]:
        pass


class RangeNumericFilter(RangeNumericMixin, admin.FieldListFilter):
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
        if not isinstance(field, DecimalField | IntegerField | FloatField | AutoField):
            raise TypeError(
                f"Class {type(self.field)} is not supported for {self.__class__.__name__}."
            )

        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        self.init_used_parameters(params)


class SliderNumericFilter(RangeNumericFilter):
    MAX_DECIMALS = 7
    STEP = None

    template = "unfold/filters/filters_numeric_slider.html"
    field = None
    form_class = SliderNumericForm

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

        self.field = field
        self.q = model_admin.get_queryset(request)

    def choices(self, changelist: ChangeList) -> Iterator:
        pass

    def _get_min_step(self, precision: int) -> float:
        pass
