# Generated by Django 3.2.18 on 2023-04-02 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xnote', '0003_auto_20230402_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xiangqigame',
            name='BLACKCLUB',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='BLACKPLAYER',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='DATE',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='EVENT',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='OPENING',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='REDCLUB',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='REDPLAYER',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='RESULT',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='ROUND',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='xiangqigame',
            name='VARIATION',
            field=models.CharField(max_length=255, null=True),
        ),
    ]