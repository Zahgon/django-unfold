from typing import TYPE_CHECKING, Any

from django.contrib.admin import helpers
from django.contrib.admin.utils import lookup_field, quote
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import (
    Field,
    FileField,
    ForeignObjectRel,
    ImageField,
    JSONField,
    ManyToManyRel,
    OneToOneField,
)
from django.forms import ModelChoiceField, ModelMultipleChoiceField, Widget
from django.forms.utils import flatatt
from django.template.defaultfilters import linebreaksbr
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.utils.html import conditional_escape, format_html
from django.utils.module_loading import import_string
from django.utils.safestring import SafeString, SafeText, mark_safe
from django.utils.text import capfirst

from unfold.settings import get_config
from unfold.utils import display_for_field, prettify_json
from unfold.widgets import (
    CHECKBOX_LABEL_CLASSES,
    LABEL_CLASSES,
    UnfoldAdminAutocompleteModelChoiceFieldWidget,
    UnfoldAdminMultipleAutocompleteModelChoiceFieldWidget,
)

if TYPE_CHECKING:
    from unfold.admin import ModelAdmin


class UnfoldAdminReadonlyField(helpers.AdminReadonlyField):
    model_admin: "ModelAdmin"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.resolved_field = self._resolve_field()

    def label_tag(self) -> SafeText:
        pass

    @property
    def url(self) -> str | bool:
        pass

    @property
    def is_json(self) -> bool:
        pass

    @property
    def is_image(self) -> bool:
        pass

    @property
    def is_file(self) -> bool:
        pass

    def contents(self) -> SafeString:
        pass

    def get_admin_url(self, remote_field, remote_obj):
        pass

    def _get_contents(self) -> SafeString:  # noqa: PLR0912
        pass

    def _preprocess_field(self, contents: SafeString) -> SafeString:
        pass

    def _resolve_field(self) -> bool | tuple[Field | None, str | None, Any]:
        pass


class UnfoldAdminField(helpers.AdminField):
    def label_tag(self) -> SafeText:
        pass


class AutocompleteFieldMixin:
    def __init__(self, url_path: str, *args: Any, **kwargs: Any) -> None:
        self.url_path = url_path
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: Widget) -> dict[str, Any]:
        pass


class UnfoldAdminAutocompleteModelChoiceField(AutocompleteFieldMixin, ModelChoiceField):
    widget = UnfoldAdminAutocompleteModelChoiceFieldWidget


class UnfoldAdminMultipleAutocompleteModelChoiceField(
    AutocompleteFieldMixin, ModelMultipleChoiceField
):
    widget = UnfoldAdminMultipleAutocompleteModelChoiceFieldWidget
