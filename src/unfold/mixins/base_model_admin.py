import copy
from typing import Any

from django.contrib.admin import helpers
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db import models
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.fields import TypedChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import SelectMultiple
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from unfold import widgets
from unfold.overrides import FORMFIELD_OVERRIDES


class BaseModelAdminMixin:
    def __init__(self, model: type[models.Model], admin_site: AdminSite) -> None:
        overrides = copy.deepcopy(FORMFIELD_OVERRIDES)

        for k, v in self.formfield_overrides.items():
            overrides.setdefault(k, {}).update(v)

        self.formfield_overrides = overrides

        super().__init__(model, admin_site)

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict[str, Any] | None = None,
    ) -> Any:
        pass

    def formfield_for_choice_field(
        self, db_field: Field, request: HttpRequest, **kwargs
    ) -> TypedChoiceField:
        pass

    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs
    ) -> ModelChoiceField | None:
        pass

    def formfield_for_manytomany(
        self,
        db_field: ManyToManyField,
        request: HttpRequest,
        **kwargs,
    ) -> ModelMultipleChoiceField:
        pass

    def formfield_for_nullboolean_field(
        self, db_field: Field, request: HttpRequest, **kwargs
    ) -> Field | None:
        pass

    def formfield_for_dbfield(
        self, db_field: Field, request: HttpRequest, **kwargs
    ) -> Field | None:
        pass
