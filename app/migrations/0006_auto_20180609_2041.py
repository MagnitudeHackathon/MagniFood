# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-09 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180609_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workplace_type', models.IntegerField(choices=[(1, 'Cafe'), (2, 'Company'), (3, 'Cafeteria')], default=2)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('block', models.CharField(blank=True, max_length=150, null=True)),
                ('floor', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='category',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='foodItem',
        ),
        migrations.RemoveField(
            model_name='fooditem',
            name='foodJoint',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='block',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='company',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='floor',
        ),
        migrations.AlterField(
            model_name='order',
            name='foodJoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foodJoint', to='app.Workplace'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'CafeUser'), (2, 'Customer'), (3, 'CafeteriaUser')], default=2),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='cafe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Workplace'),
        ),
        migrations.AddField(
            model_name='profile',
            name='workplace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Workplace'),
        ),
    ]