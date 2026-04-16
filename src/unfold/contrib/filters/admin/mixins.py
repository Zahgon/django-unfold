from collections.abc import Callable, Iterator
from typing import Any

from django.contrib.admin import (
    ChoicesFieldListFilter,
    ListFilter,
    RelatedFieldListFilter,
)
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models import QuerySet
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.fields.related import RelatedField
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from unfold.contrib.filters.forms import (
    AutocompleteDropdownForm,
    CheckboxForm,
    DropdownForm,
    RadioForm,
    RangeNumericForm,
)


class ValueMixin:
    lookup_val = None

    def value(self) -> str | None:
        if isinstance(self.lookup_val, list) and len(self.lookup_val):
            return self.lookup_val[0]

        return self.lookup_val


class MultiValueMixin:
    lookup_val = None

    def value(self) -> list[str] | None:
        return self.lookup_val


class DropdownMixin:
    template = "unfold/filters/filters_field.html"
    form_class = DropdownForm
    all_option = ["", _("All")]


class ChoicesMixin(ChoicesFieldListFilter):
    template = "unfold/filters/filters_field.html"
    all_option: tuple[str, str] | None = None
    form_class: type[CheckboxForm | RadioForm]
    value: Callable

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class RangeNumericMixin(ListFilter):
    request = None
    template = "unfold/filters/filters_numeric_range.html"
    parameter_name: str | None = None

    def init_used_parameters(self, params: dict[str, Any]) -> None:
        pass

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        pass

    def expected_parameters(self) -> list[str | None]:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass


class AutocompleteMixin(RelatedFieldListFilter):
    model_admin: ModelAdmin
    form_class: type[AutocompleteDropdownForm]
    value: Callable

    def has_output(self) -> bool:
        pass

    def field_choices(
        self, field: RelatedField, request: HttpRequest, model_admin: ModelAdmin
    ) -> list[tuple]:
        pass

    def choices(self, changelist: ChangeList) -> Iterator:
        pass
