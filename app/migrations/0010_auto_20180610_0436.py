# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-09 23:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20180609_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('foodItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.FoodItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='foodItems1',
            field=models.ManyToManyField(blank=True, null=True, related_name='foodItem', through='app.OrderDetail', to='app.FoodItem'),
        ),
    ]
