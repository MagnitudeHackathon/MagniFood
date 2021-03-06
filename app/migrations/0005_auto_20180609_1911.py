# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-09 13:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_remove_category_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_status', models.IntegerField(choices=[(1, 'Ordered'), (2, 'Confirmed'), (3, 'Ready'), (4, 'Delivered')], default=1)),
                ('price', models.FloatField(default=0.0)),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fooditem',
            name='availableQuantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='foodItem',
            field=models.ManyToManyField(blank=True, null=True, to='app.FoodItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='foodItems',
            field=models.ManyToManyField(blank=True, null=True, to='app.FoodItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='foodJoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foodJoint', to=settings.AUTH_USER_MODEL),
        ),
    ]
