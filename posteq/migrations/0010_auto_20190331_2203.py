# Generated by Django 2.1.5 on 2019-03-31 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posteq', '0009_auto_20190310_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='EqActiveTeniSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100, null=True)),
                ('ability', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posteq.TeniSkillBase')),
            ],
        ),
        migrations.CreateModel(
            name='EqVariousData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_str', models.CharField(blank=True, max_length=200, null=True)),
                ('skill_str', models.CharField(blank=True, max_length=300, null=True)),
                ('teniskill_str', models.CharField(blank=True, max_length=200, null=True)),
                ('senyuskill_str', models.CharField(blank=True, max_length=200, null=True)),
                ('Nskill', models.IntegerField(default=0)),
                ('Nslot', models.IntegerField(default=0)),
                ('NZP', models.IntegerField(default=0)),
                ('Nkiwami', models.IntegerField(default=0)),
                ('Nshin', models.IntegerField(default=0)),
                ('Nfes', models.IntegerField(default=0)),
                ('Nevent', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='eqactiveability',
            name='active',
        ),
        migrations.RemoveField(
            model_name='eqactiveability',
            name='type',
        ),
        migrations.AlterField(
            model_name='eq',
            name='active_abilities',
            field=models.ManyToManyField(blank=True, related_name='active_abilities_in_eq', to='posteq.EqActiveAbility'),
        ),
        migrations.AddField(
            model_name='eq',
            name='active_teni_skills',
            field=models.ManyToManyField(blank=True, related_name='active_teni_skills_in_eq', to='posteq.EqActiveTeniSkill'),
        ),
        migrations.AddField(
            model_name='eq',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posteq.EqVariousData'),
        ),
    ]
