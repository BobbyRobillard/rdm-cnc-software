# Generated by Django 2.0 on 2019-02-05 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20190205_0200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lense',
            old_name='focus_diameter',
            new_name='diameter',
        ),
        migrations.RenameField(
            model_name='lense',
            old_name='focus_height',
            new_name='height',
        ),
        migrations.RemoveField(
            model_name='lense',
            name='custom_focus_band_size',
        ),
        migrations.RemoveField(
            model_name='lense',
            name='custom_zoom_band_size',
        ),
        migrations.RemoveField(
            model_name='lense',
            name='zoom_diameter',
        ),
        migrations.RemoveField(
            model_name='lense',
            name='zoom_height',
        ),
        migrations.AddField(
            model_name='lense',
            name='custom_band_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.StandardBandit'),
        ),
    ]
