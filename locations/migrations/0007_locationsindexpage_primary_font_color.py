# Generated by Django 3.1.4 on 2021-02-03 22:43

from django.db import migrations
import wagtail_color_panel.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20210203_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationsindexpage',
            name='primary_font_color',
            field=wagtail_color_panel.fields.ColorField(default='#FFFFFF', max_length=7),
        ),
    ]