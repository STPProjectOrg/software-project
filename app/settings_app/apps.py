""" 
Settings app config. 
"""

from django.apps import AppConfig


class SettingsAppConfig(AppConfig):
    """
    This class represents the settings app config.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings_app'
