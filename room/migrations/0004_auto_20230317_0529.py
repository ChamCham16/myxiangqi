# Generated by Django 3.2.18 on 2023-03-16 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_auto_20230317_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xiangqiroom',
            name='black',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='xiangqiroom',
            name='board',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='xiangqiroom',
            name='turn',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='xiangqiroom',
            name='white',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='xiangqiroom',
            name='winner',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
