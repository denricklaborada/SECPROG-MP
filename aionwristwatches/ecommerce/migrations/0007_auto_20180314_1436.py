# Generated by Django 2.0.3 on 2018-03-14 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_auto_20180312_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prodname',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
