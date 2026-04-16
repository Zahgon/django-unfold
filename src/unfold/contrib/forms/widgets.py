from typing import Any

from django.core.validators import EMPTY_VALUES
from django.forms import MultiWidget, Widget
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from unfold.widgets import (
    PROSE_CLASSES,
    UnfoldAdminSelectWidget,
    UnfoldAdminTextInputWidget,
)

WYSIWYG_CLASSES = [
    *PROSE_CLASSES,
    "border!",
    "border-base-200!",
    "border-t-0!",
    "group-[.errors]:border-red-600",
    "max-w-none",
    "p-4",
    "rounded-b",
    "rounded-t-none",
    "text-base-500",
    "w-full",
    "focus:outline-hidden",
    "dark:border-base-700!",
    "dark:text-base-300!",
    "dark:group-[.errors]:border-red-500!",
]


class ArrayWidget(MultiWidget):
    template_name = "unfold/forms/array.html"

    def __init__(
        self,
        widget_class: type[Widget] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.choices = kwargs.get("choices")
        self.widget_class = widget_class

        widgets = [self.get_widget_instance()]
        super().__init__(widgets, attrs=kwargs.get("attrs", None))

    def get_widget_instance(self) -> Any:
        pass

    def get_context(self, name: str, value: Any, attrs: dict | None) -> dict:
        pass

    def value_from_datadict(
        self, data: QueryDict, files: MultiValueDict, name: str
    ) -> list:  # ty:ignore[invalid-method-override]
        pass

    def value_omitted_from_data(
        self, data: QueryDict, files: MultiValueDict, name: str
    ) -> bool:  # ty:ignore[invalid-method-override]
        pass

    def decompress(self, value: Any) -> list:
        pass

    def _resolve_widgets(self, value: list | str | None) -> None:
        pass


class WysiwygWidget(Widget):
    template_name = "unfold/forms/wysiwyg.html"

    class Media:
        css = {"all": ("unfold/forms/css/trix/trix.css",)}
        js = (
            "unfold/forms/js/trix/trix.js",
            "unfold/forms/js/trix.config.js",
        )

    def __init__(self, attrs: dict[str, Any] | None = None) -> None:
        super().__init__(attrs)

        self.attrs.update(
            {
                "class": " ".join(
                    [*WYSIWYG_CLASSES, attrs.get("class", "") if attrs else ""]
                )
            }
        )
