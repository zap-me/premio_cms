# Generated by Django 3.1.4 on 2021-01-08 23:25

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('locations', '0002_lat_long'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationsindexpage',
            name='max_dist_km',
            field=models.IntegerField(default=50, verbose_name='maximum distance (km)'),
        ),
        migrations.AddField(
            model_name='locationsindexpage',
            name='show_near_me',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='lat_long',
            field=models.CharField(blank=True, max_length=30, verbose_name='Latitude, longitude'),
        ),
        migrations.CreateModel(
            name='LocationsIndexPromotedPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='promoted_pages', to='locations.locationsindexpage')),
                ('promoted_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
