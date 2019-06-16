"""App config."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserConfig(AppConfig):
    """Register user app."""

    name = 'djangoui.user'
    verbose_name = _('profiles')

    def ready(self):
        """Register a signal."""
        import djangoui.user.signals  # noqa
