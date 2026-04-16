from functools import partial
from typing import Any

from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.utils import NestedObjects, flatten_fieldsets
from django.core.exceptions import ValidationError
from django.db import router
from django.db.models import Model, QuerySet
from django.forms.formsets import DELETION_FIELD_NAME
from django.forms.models import ALL_FIELDS, modelform_defines_fields
from django.http import HttpRequest
from django.utils.text import get_text_list
from django.utils.translation import gettext_lazy as _

from unfold.admin import StackedInline, TabularInline
from unfold.contrib.inlines.checks import NonrelatedModelAdminChecks
from unfold.contrib.inlines.forms import (
    NonrelatedInlineModelFormSet,
    nonrelated_inline_formset_factory,
)


class NonrelatedInlineMixin(InlineModelAdmin):
    checks_class = NonrelatedModelAdminChecks
    formset = NonrelatedInlineModelFormSet

    def get_formset(
        self, request: HttpRequest, obj: Model | None = None, **kwargs: Any
    ):
        pass

    def get_form_queryset(self, obj: Model) -> QuerySet:
        raise NotImplementedError("get_form_queryset must be implemented")

    def save_new_instance(self, parent: Model, instance: Model) -> None:
        raise NotImplementedError("save_new_instance must be implemented")

    def _get_formset_defaults(
        self, request: HttpRequest, obj: Model | None = None, **kwargs: Any
    ):
        """Return a BaseInlineFormSet class for use in admin add/change views."""
        pass


class NonrelatedStackedInline(NonrelatedInlineMixin, StackedInline):
    formset = NonrelatedInlineModelFormSet


class NonrelatedTabularInline(NonrelatedInlineMixin, TabularInline):
    formset = NonrelatedInlineModelFormSet
