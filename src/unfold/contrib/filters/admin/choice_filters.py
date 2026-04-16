from collections.abc import Iterator
from typing import Any

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Model
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin.mixins import (
    ChoicesMixin,
    MultiValueMixin,
    ValueMixin,
)
from unfold.contrib.filters.forms import CheckboxForm, HorizontalRadioForm, RadioForm


class RadioFilter(admin.SimpleListFilter):
    template = "unfold/filters/filters_field.html"
    form_class = RadioForm
    all_option = ["", _("All")]

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class CheckboxFilter(RadioFilter):
    form_class = CheckboxForm
    all_option = None

    # TODO: remove once django 4.x is not supported
    def __init__(
        self,
        request: HttpRequest,
        params: dict[str, Any],
        model: type[Model],
        model_admin: ModelAdmin,
    ) -> None:
        self.request = request
        super().__init__(request, params, model, model_admin)

    def value(self) -> list[str] | None:  # ty:ignore[invalid-method-override]
        if self.parameter_name:
            return self.request.GET.getlist(self.parameter_name)


class ChoicesRadioFilter(ValueMixin, ChoicesMixin, admin.ChoicesFieldListFilter):
    form_class = RadioForm
    all_option = ["", _("All")]


class ChoicesCheckboxFilter(
    MultiValueMixin, ChoicesMixin, admin.ChoicesFieldListFilter
):
    form_class = CheckboxForm
    all_option = None


class BooleanRadioFilter(ValueMixin, admin.BooleanFieldListFilter):
    template = "unfold/filters/filters_field.html"
    form_class = HorizontalRadioForm
    all_option = ["", _("All")]

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class RelatedCheckboxFilter(MultiValueMixin, admin.RelatedFieldListFilter):
    template = "unfold/filters/filters_field.html"
    form_class = CheckboxForm

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class AllValuesCheckboxFilter(MultiValueMixin, admin.AllValuesFieldListFilter):
    template = "unfold/filters/filters_field.html"
    form_class = CheckboxForm

    def choices(self, changelist: ChangeList) -> Iterator:
        pass
