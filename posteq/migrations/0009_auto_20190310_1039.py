# Generated by Django 2.1.5 on 2019-03-10 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posteq', '0008_auto_20190228_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='EqActiveAbility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ability', models.CharField(max_length=20, null=True)),
                ('type', models.CharField(max_length=20, null=True)),
                ('point', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=20, null=True)),
                ('active', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='eq',
            name='active_teni_skills',
        ),
        migrations.RemoveField(
            model_name='eq',
            name='deactive_skills',
        ),
        migrations.RemoveField(
            model_name='eq',
            name='passive_skills',
        ),
        migrations.RemoveField(
            model_name='eq',
            name='skill_points',
        ),
        migrations.RemoveField(
            model_name='eq',
            name='skill_teni_points',
        ),
        migrations.AddField(
            model_name='eqactiveskill',
            name='active',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='eqactiveskill',
            name='point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eqactiveskill',
            name='skill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posteq.SkillBase'),
        ),
        migrations.DeleteModel(
            name='EqSkillPoint',
        ),
        migrations.AddField(
            model_name='eq',
            name='active_abilities',
            field=models.ManyToManyField(blank=True, related_name='active_teni_skills_in_eq', to='posteq.EqActiveAbility'),
        ),
    ]