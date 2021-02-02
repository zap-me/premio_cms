# Generated by Django 3.1.4 on 2021-02-02 22:39

from django.db import migrations
import wagtail_color_panel.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_promoted_pages_title_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationsindexpage',
            name='page_theme_color',
            field=wagtail_color_panel.fields.ColorField(default='#007bf', max_length=7),
        ),
    ]
