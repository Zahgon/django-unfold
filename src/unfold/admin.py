from functools import update_wrapper
from typing import Any

from django import forms
from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.contrib.admin import StackedInline as BaseStackedInline
from django.contrib.admin import TabularInline as BaseTabularInline
from django.contrib.admin import display, helpers
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.contenttypes.admin import (
    GenericStackedInline as BaseGenericStackedInline,
)
from django.contrib.contenttypes.admin import (
    GenericTabularInline as BaseGenericTabularInline,
)
from django.db.models import BLANK_CHOICE_DASH, Model
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import URLPattern, path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views import View

from unfold.checks import UnfoldModelAdminChecks
from unfold.datasets import BaseDataset
from unfold.forms import (
    ActionForm,
    PaginationGenericInlineFormSet,
    PaginationInlineFormSet,
)
from unfold.mixins import (
    ActionModelAdminMixin,
    BaseModelAdminMixin,
    DatasetModelAdminMixin,
    NestedInlinesModelAdminMixin,
)
from unfold.overrides import FORMFIELD_OVERRIDES_INLINE
from unfold.typing import FieldsetsType
from unfold.views import ChangeList
from unfold.widgets import UnfoldBooleanWidget

checkbox = UnfoldBooleanWidget(
    {
        "class": "action-select",
        "aria-label": _("Select record"),
    },
    lambda value: False,
)


class ModelAdmin(
    BaseModelAdminMixin,
    ActionModelAdminMixin,
    DatasetModelAdminMixin,
    NestedInlinesModelAdminMixin,
    BaseModelAdmin,
):
    action_form = ActionForm
    custom_urls = ()
    add_fieldsets = ()
    ordering_field = None
    hide_ordering_field = False
    list_horizontal_scrollbar_top = False
    list_filter_submit = False
    list_filter_sheet = True
    list_fullwidth = False
    list_disable_select_all = False
    list_before_template = None
    list_after_template = None
    change_form_before_template = None
    change_form_after_template = None
    change_form_outer_before_template = None
    change_form_outer_after_template = None
    change_form_datasets = ()
    compressed_fields = True
    show_add_link = True
    readonly_preprocess_fields = {}
    warn_unsaved_form = False
    checks_class = UnfoldModelAdminChecks

    @property
    def media(self):
        pass

    def changelist_view(
        self, request: HttpRequest, extra_context: dict[str, str] | None = None
    ) -> TemplateResponse:
        pass

    def get_list_display(self, request: HttpRequest) -> list | tuple:
        pass

    def get_fieldsets(
        self, request: HttpRequest, obj: Model | None = None
    ) -> FieldsetsType:
        pass

    def get_custom_urls(self) -> tuple[tuple[str, str, View], ...]:
        """
        Method to get custom views for ModelAdmin with their urls

        Format of custom_urls item:
            ("path_to_view", "name_of_view", view_itself)
        """
        pass

    def get_urls(self) -> list[URLPattern]:
        pass

    def _path_from_custom_url(self, custom_url: tuple[str, str, View]) -> URLPattern:
        pass

    def get_action_choices(
        self,
        request: HttpRequest,
        default_choices: list[tuple[str, str]] = BLANK_CHOICE_DASH,
    ) -> list[tuple[str, str]]:
        pass

    @display(description=mark_safe(checkbox.render("action_toggle_all", 1)))
    def action_checkbox(self, obj: Model) -> str:
        pass

    def get_changelist(self, request: HttpRequest, **kwargs: Any) -> ChangeList:
        pass

    def get_formset_kwargs(
        self, request: HttpRequest, obj: Model, inline: InlineModelAdmin, prefix: str
    ) -> dict[str, Any]:
        pass

    def get_changeform_datasets(self, request: HttpRequest) -> list[type[BaseDataset]]:
        pass


class BaseInlineMixin:
    formfield_overrides = FORMFIELD_OVERRIDES_INLINE
    readonly_preprocess_fields = {}
    ordering_field = None
    per_page = None
    hide_ordering_field = False
    collapsible = False
    show_count = False
    hide_title = False
    tab = False


class TabularInline(BaseInlineMixin, BaseModelAdminMixin, BaseTabularInline):
    formset = PaginationInlineFormSet


class StackedInline(BaseInlineMixin, BaseModelAdminMixin, BaseStackedInline):
    formset = PaginationInlineFormSet


class GenericStackedInline(
    BaseInlineMixin, BaseModelAdminMixin, BaseGenericStackedInline
):
    formset = PaginationGenericInlineFormSet


class GenericTabularInline(
    BaseInlineMixin, BaseModelAdminMixin, BaseGenericTabularInline
):
    formset = PaginationGenericInlineFormSet
