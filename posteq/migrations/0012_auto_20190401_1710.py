# Generated by Django 2.1.5 on 2019-04-01 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posteq', '0011_auto_20190401_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuffsineq',
            old_name='Cuff_data',
            new_name='cuff_data',
        ),
        migrations.RenameField(
            model_name='jewelsineq',
            old_name='Jewel_data',
            new_name='jewel_data',
        ),
    ]