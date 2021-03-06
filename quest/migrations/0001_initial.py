# Generated by Django 2.1.5 on 2019-05-19 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posteq', '0016_auto_20190404_2023'),
        ('user', '0003_auto_20190428_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallFor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_pos_date', models.DateTimeField(null=True, verbose_name='投稿日時')),
                ('request_text', models.CharField(blank=True, max_length=400, null=True)),
                ('if_condition_on', models.BooleanField(default=True)),
                ('answer_due_date', models.DateTimeField(null=True)),
                ('answers', models.ManyToManyField(blank=True, to='posteq.EQ')),
                ('best_answer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='best_eq_of', to='posteq.EQ')),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='RequestedSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_greater', models.BooleanField(default=False)),
                ('skill_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posteq.SkillBase')),
                ('skill_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posteq.SkillDetail')),
            ],
        ),
        migrations.CreateModel(
            name='RequestedTeniSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_greater', models.BooleanField(default=False)),
                ('skill_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posteq.TeniSkillBase')),
                ('skill_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posteq.AbilityDetail')),
            ],
        ),
        migrations.AddField(
            model_name='callfor',
            name='requested_skills',
            field=models.ManyToManyField(blank=True, to='quest.RequestedSkill'),
        ),
        migrations.AddField(
            model_name='callfor',
            name='requested_teniskills',
            field=models.ManyToManyField(blank=True, to='quest.RequestedTeniSkill'),
        ),
        migrations.AddField(
            model_name='callfor',
            name='wep_kind',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posteq.WepKind'),
        ),
    ]
