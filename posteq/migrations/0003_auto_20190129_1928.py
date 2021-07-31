# Generated by Django 2.0.8 on 2019-01-29 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posteq', '0002_auto_20190129_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eqdata',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posteq.DataOfEq'),
        ),
        migrations.AlterField(
            model_name='eqdata',
            name='element',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posteq.Elemental'),
        ),
    ]
