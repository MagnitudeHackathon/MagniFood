# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-10 00:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180610_0555'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngridientDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('foodItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.FoodItem')),
            ],
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='availableQuantity',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='ingridientdetail',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Ingredients'),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='ingridients1',
            field=models.ManyToManyField(blank=True, null=True, related_name='ingridients', through='app.IngridientDetail', to='app.Ingredients'),
        ),
    ]
