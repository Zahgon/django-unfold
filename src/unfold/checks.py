from typing import Any

from django.contrib.admin.checks import ModelAdminChecks
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.models import Permission
from django.core import checks

from unfold.dataclasses import UnfoldAction


class UnfoldModelAdminChecks(ModelAdminChecks):
    def check(self, admin_obj: BaseModelAdmin, **kwargs) -> list[checks.Error]:
        pass

    def _check_unfold_action_permission_methods(self, obj: Any) -> list[checks.Error]:
        """
        Actions with an allowed_permission attribute require the ModelAdmin to
        implement a has_<perm>_permission() method for each permission.
        """
        pass
