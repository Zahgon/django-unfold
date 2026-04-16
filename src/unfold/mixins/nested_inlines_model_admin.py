from typing import Any

from django.contrib.admin import options
from django.contrib.admin.helpers import InlineAdminFormSet
from django.contrib.admin.options import InlineModelAdmin
from django.db.models import Model
from django.forms import BaseInlineFormSet, Media, ModelForm
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _


def nested_all_valid(formsets: list[BaseInlineFormSet]) -> bool:
    pass


class NestedInlinesModelAdminMixin:
    # Build custom media for all nested formsets and process it
    # later in media property in ModelAdmin
    nested_formset_media = Media()

    def _create_formsets(
        self, request: HttpRequest, obj: Model | None = None, change: bool = False
    ) -> tuple[list[BaseInlineFormSet], list[InlineModelAdmin]]:
        pass

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict[str, Any] | None = None,
    ) -> HttpResponse:
        # Monkey patch all_valid to do nested formsets validation. Applied because
        # we don't want to completely override `BaseModelAdmin._changeform_view()`
        pass

    def save_formset(
        self,
        request: HttpRequest,
        form: ModelForm,
        formset: BaseInlineFormSet,
        change: bool,
    ) -> None:
        pass

    def _build_nested_formsets(
        self,
        request: HttpRequest,
        obj: Model,
        formsets: list[BaseInlineFormSet],
        inline_instances: list[InlineModelAdmin],
        change: bool,
    ) -> None:
        pass

    def _get_nested_formset(
        self,
        request: HttpRequest,
        obj: Model,
        form: ModelForm,
        parent_inline: InlineModelAdmin,
        inline_class: type[InlineModelAdmin],
        change: bool,
    ) -> InlineAdminFormSet | None:
        pass

    def _check_nested_inline_permissions(
        self,
        request: HttpRequest,
        inline: InlineModelAdmin,
        obj: Model | None = None,
    ) -> bool:
        pass

    def _user_deleted_form(
        self,
        prefix: str,
        request: HttpRequest,
        inline: InlineModelAdmin,
        obj: Model,
        index: int,
    ) -> bool:
        pass

    def _nested_inline_permissions(
        self,
        request: HttpRequest,
        inline: InlineModelAdmin,
        inline_formset: BaseInlineFormSet,
        obj: Model,
    ) -> dict[str, bool]:
        pass
