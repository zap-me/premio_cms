from django.db import models
from wagtail.core.models import Page
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel

class HomePage(Page):
    pass



