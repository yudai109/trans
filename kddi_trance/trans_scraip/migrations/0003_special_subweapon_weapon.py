# Generated by Django 3.2.7 on 2021-10-05 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trans_scraip', '0002_delete_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='名前')),
                ('overview', models.TextField(blank=True, verbose_name='概要')),
            ],
            options={
                'verbose_name': 'スペシャル',
                'verbose_name_plural': 'スペシャル一覧',
            },
        ),
        migrations.CreateModel(
            name='SubWeapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='名前')),
                ('overview', models.TextField(blank=True, verbose_name='概要')),
            ],
            options={
                'verbose_name': 'サブウェポン',
                'verbose_name_plural': 'サブウェポン一覧',
            },
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField(blank=True, null=True, verbose_name='番号')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='ブキ名')),
                ('category', models.CharField(blank=True, choices=[('0', 'シューター'), ('1', 'マニューバー'), ('2', 'ブラスター'), ('3', 'スピナー'), ('4', 'ローラー'), ('5', 'フデ'), ('6', 'チャージャー'), ('7', 'スロッシャー'), ('8', 'シェルター'), ('9', 'ガイザー')], max_length=2)),
                ('gauge', models.IntegerField(blank=True, null=True, verbose_name='スペシャル必要ポイント')),
                ('release_condition', models.CharField(blank=True, max_length=100, verbose_name='解放条件')),
                ('range', models.IntegerField(blank=True, null=True, verbose_name='射程')),
                ('continuous_power', models.IntegerField(blank=True, null=True, verbose_name='連射力')),
                ('fixed_num', models.IntegerField(blank=True, null=True, verbose_name='確定数')),
                ('special', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='trans_scraip.special')),
                ('sub', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='trans_scraip.subweapon')),
            ],
            options={
                'verbose_name': 'ブキ',
                'verbose_name_plural': 'ブキ一覧',
            },
        ),
    ]
