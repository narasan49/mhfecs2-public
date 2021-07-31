# Generated by Django 2.1.5 on 2019-04-03 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posteq', '0014_eq_posted_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateHist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True, verbose_name='更新日時')),
                ('datver', models.CharField(blank=True, max_length=20, null=True)),
                ('errors', models.CharField(blank=True, max_length=1000, null=True)),
                ('others', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
    ]
