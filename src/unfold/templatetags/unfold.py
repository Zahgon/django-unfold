import json
from collections.abc import Iterable, Mapping
from typing import Any

from django import VERSION as DJANGO_VERSION
from django import template
from django.contrib.admin.helpers import (
    AdminField,
    AdminForm,
    AdminReadonlyField,
    Fieldset,
    InlineAdminFormSet,
)
from django.contrib.admin.views.main import PAGE_VAR, ChangeList
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.auth.models import AbstractUser
from django.core.paginator import Paginator
from django.db.models import Model
from django.db.models.options import Options
from django.forms import BoundField, CheckboxSelectMultiple
from django.http import HttpRequest, QueryDict
from django.template import Context, Library, Node, RequestContext, TemplateSyntaxError
from django.template.base import NodeList, Parser, Token, token_kwargs
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from unfold.components import ComponentRegistry
from unfold.enums import ActionVariant
from unfold.sections import BaseSection
from unfold.utils import prettify_traceback
from unfold.widgets import (
    UnfoldAdminMoneyWidget,
    UnfoldAdminSelect2Widget,
    UnfoldAdminSplitDateTimeWidget,
)

register = Library()


def _count_errors_in_general(
    admin_form: AdminForm, inlines: list[InlineAdminFormSet]
) -> int:
    pass


def _count_errors_in_inline(inline: InlineAdminFormSet) -> int:
    pass


def _get_tabs_list(
    context: RequestContext, page: str, opts: Options | None = None
) -> list:
    pass


@register.simple_tag(name="action_list", takes_context=True)
def action_list(context: RequestContext) -> str:
    pass


@register.simple_tag(name="tab_list", takes_context=True)
def tab_list(context: RequestContext, page: str, opts: Options | None = None) -> str:
    pass


@register.simple_tag(name="render_section", takes_context=True)
def render_section(
    context: RequestContext, section_class: type[BaseSection] | str, instance: Model
) -> str:
    pass


@register.simple_tag(name="has_nav_item_active")
def has_nav_item_active(items: list) -> bool:
    pass


@register.filter
def has_active_item(items: list[dict]) -> bool:
    pass


@register.filter
def class_name(value: Any) -> str:
    pass


@register.filter
def is_list(value: Any) -> bool:
    pass


@register.filter
def index(indexable: Mapping[int, Any], i: int) -> Any:
    pass


@register.filter
def tabs(adminform: AdminForm) -> list[Fieldset]:
    pass


def _flatten_context(context: Context) -> dict[str, Any]:
    """
    Return the template context as a single flat dict.
    On Django < 5, context.flatten() can raise ValueError for contexts
    created with context.new() (Django #35417). Use a safe implementation.
    """
    if DJANGO_VERSION >= (5, 0):
        return context.flatten()
    # TODO: remove once Django 4.2 is not supported
    # Django 4.2: build flat dict by resolving keys, avoid context.flatten()
    keys = set()
    for d in context.dicts:
        if hasattr(d, "keys"):
            keys.update(d.keys())
    return {k: context[k] for k in keys}


class RenderComponentNode(template.Node):
    def __init__(
        self,
        template_name: str,
        nodelist: NodeList,
        extra_context: dict | None = None,
        include_context: bool = False,
        *args,
        **kwargs,
    ):
        self.template_name = template_name
        self.nodelist = nodelist
        self.extra_context = extra_context or {}
        self.include_context = include_context
        super().__init__(*args, **kwargs)

    def render(self, context: Context) -> str:
        values = {
            name: var.resolve(context) for name, var in self.extra_context.items()
        }
        request = context.request if isinstance(context, RequestContext) else None

        if "component_class" in values:
            values = ComponentRegistry.create_instance(
                values["component_class"], request=request
            ).get_context_data(**values)

        context_copy = context.new()
        context_copy.update(_flatten_context(context))
        context_copy.update(values)
        children = self.nodelist.render(context_copy)

        if len(children) > 0:
            values.update(
                {
                    "children": children,
                }
            )

        if self.include_context:
            values.update(_flatten_context(context))

        return render_to_string(self.template_name, request=request, context=values)


@register.tag("component")
def do_component(parser: Parser, token: Token) -> RenderComponentNode:
    pass


@register.filter
def add_css_class(field: BoundField, classes: list | tuple) -> BoundField:
    pass


@register.inclusion_tag(
    "unfold/templatetags/preserve_changelist_filters.html",
    takes_context=True,
    name="preserve_filters",
)
def preserve_changelist_filters(context: RequestContext) -> dict[str, dict[str, str]]:
    """
    Generate hidden input fields to preserve filters for POST forms.
    """
    pass


@register.simple_tag(takes_context=True)
def element_classes(context: RequestContext, key: str) -> str:
    pass


@register.simple_tag(takes_context=True)
def fieldset_rows_classes(context: RequestContext) -> str:
    pass


@register.simple_tag(takes_context=True)
def fieldset_row_classes(context: RequestContext) -> str:
    pass


@register.simple_tag(takes_context=True)
def fieldset_line_classes(context: RequestContext) -> str:
    pass


@register.simple_tag(takes_context=True)
def action_item_classes(context: RequestContext, action: dict) -> str:
    pass


@register.filter
def changeform_data(adminform: AdminForm) -> str:
    pass


@register.filter
def changeform_condition(
    field: AdminField | AdminReadonlyField,
) -> AdminField | AdminReadonlyField:
    pass


@register.simple_tag
def infinite_paginator_url(cl, i):
    pass


@register.simple_tag
def elided_page_range(paginator: Paginator, number: int) -> Iterable[int | str] | None:
    pass


@register.simple_tag(takes_context=True)
def querystring_params(
    context: RequestContext, query_key: str, query_value: str
) -> str:
    pass


@register.simple_tag(name="unfold_querystring", takes_context=True)
def unfold_querystring(context, *args, **kwargs):
    """
    Duplicated querystring template tag from Django core to allow
    it using in Django 4.x.
    TODO: Once 4.x is not supported, remove it.
    """
    pass


@register.simple_tag(takes_context=True)
def header_title(context: RequestContext) -> str:
    pass


@register.simple_tag(takes_context=True)
def admin_object_app_url(context: RequestContext, object: Model, arg: str) -> str:
    pass


@register.filter
def has_nested_tables(table: dict) -> bool:
    pass


@register.filter
def inline_add_button_text(json_string: str) -> str:
    pass


class RenderCaptureNode(Node):
    def __init__(self, nodelist: NodeList, variable_name: str, silent: bool) -> None:
        self.nodelist = nodelist
        self.variable_name = variable_name
        self.silent = silent

    def render(self, context: Context) -> str:
        content = self.nodelist.render(context)

        if not self.silent:
            return content

        context.update(
            {
                self.variable_name: content,
            }
        )

        return ""


@register.tag(name="capture")
def do_capture(parser: Parser, token: Token) -> RenderCaptureNode:
    pass


@register.filter
def tabs_active(fieldsets: list[Fieldset]) -> str:
    pass


@register.filter
def tabs_errors_count(fieldset: Fieldset) -> int:
    pass


@register.simple_tag
def tabs_primary_active(inlines: list[InlineAdminFormSet]) -> str:
    pass


@register.filter
def unicoded_slugify(value: str) -> str:
    pass


@register.filter
def format_traceback(traceback: str) -> str:
    pass
