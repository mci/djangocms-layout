from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class LayoutToolsConfig(AppConfig):
    name = 'djangocms_layouttools'
    verbose_name = _('Layout Tools')
