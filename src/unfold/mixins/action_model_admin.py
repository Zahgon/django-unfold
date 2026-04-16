from collections.abc import Callable
from typing import Any

from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse

from unfold.dataclasses import UnfoldAction
from unfold.enums import ActionVariant
from unfold.exceptions import UnfoldException


class ActionModelAdminMixin:
    """
    Adds support for various ModelAdmin actions (list, detail, row, submit line)
    """

    actions_list = ()  # Displayed in changelist at the top
    actions_list_hide_default = False
    actions_row = ()  # Displayed in changelist for each row in the table
    actions_detail = ()  # Displayed in changeform at the top
    actions_detail_hide_default = False
    actions_submit_line = ()  # Displayed in changeform in the submit line (form buttons)

    def changelist_view(
        self, request: HttpRequest, extra_context: dict[str, str] | None = None
    ) -> TemplateResponse:
        """
        Changelist contains `actions_list` and `actions_row` custom actions. In case of `actions_row` they
        are displayed in the each row of the table.
        """
        pass

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict[str, Any] | None = None,
    ) -> Any:
        """
        Changeform contains `actions_submit_line` and `actions_detail` custom actions.
        """
        pass

    def save_model(
        self, request: HttpRequest, obj: Model, form: Form, change: Any
    ) -> None:
        """
        When saving object, run all appropriate actions from `actions_submit_line`
        """
        pass

    def get_unfold_action(self, action: str) -> UnfoldAction:
        """
        Converts action name into UnfoldAction object.
        """
        pass

    def get_actions_list(self, request: HttpRequest) -> list[UnfoldAction]:
        """
        Filters `actions_list` by permissions and returns list of UnfoldAction objects.
        """
        pass

    def get_actions_detail(
        self, request: HttpRequest, object_id: int
    ) -> list[UnfoldAction]:
        """
        Filters `actions_detail` by permissions and returns list of UnfoldAction objects.
        """
        pass

    def get_actions_row(self, request: HttpRequest) -> list[UnfoldAction]:
        """
        Filters `actions_row` by permissions and returns list of UnfoldAction objects.
        """
        pass

    def get_actions_submit_line(
        self, request: HttpRequest, object_id: int
    ) -> list[UnfoldAction]:
        """
        Filters `actions_submit_line` by permissions and returns list of UnfoldAction objects.
        """
        pass

    def _extract_action_names(self, actions: list[str | dict]) -> list[str]:
        """
        Gets the list of only actions names from the actions structure provided in ModelAdmin
        """
        results = []

        for action in actions or []:
            if isinstance(action, dict) and "items" in action:
                results.extend(action["items"])
            else:
                results.append(action)

        return results

    def _get_base_actions_list(self) -> list[UnfoldAction]:
        """
        Returns list of UnfoldAction objects for `actions_list`.
        """
        pass

    def _get_base_actions_detail(self) -> list[UnfoldAction]:
        """
        Returns list of UnfoldAction objects for `actions_detail`.
        """
        pass

    def _get_base_actions_row(self) -> list[UnfoldAction]:
        """
        Returns list of UnfoldAction objects for `actions_row`.
        """
        pass

    def _get_base_actions_submit_line(self) -> list[UnfoldAction]:
        """
        Returns list of UnfoldAction objects for `actions_submit_line`.
        """
        pass

    def _get_instance_method(self, method_name: str) -> Callable:
        """
        Searches for method on self instance based on method_name and returns it if it exists.
        If it does not exist or is not callable, it raises UnfoldException
        """
        pass

    def _get_actions_navigation(
        self,
        provided_actions: list[str | dict],
        allowed_actions: list[UnfoldAction],
        object_id: str | None = None,
    ) -> list[str | dict]:
        """
        Builds navigation structure for the actions which is going to be provided to the template.
        """
        pass

    def _filter_unfold_actions_by_permissions(
        self,
        request: HttpRequest,
        actions: list[UnfoldAction],
        object_id: int | str | None = None,
    ) -> list[UnfoldAction]:
        """
        Filters out actions that the user doesn't have access to.
        """
        pass
