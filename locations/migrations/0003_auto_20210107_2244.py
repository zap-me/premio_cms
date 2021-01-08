# Generated by Django 3.1.4 on 2021-01-07 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20210107_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationPromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_type', models.CharField(max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='locationpage',
            name='promotions',
            field=models.ManyToManyField(to='locations.LocationPromotion'),
        ),
    ]
