# Generated by Django 2.0.3 on 2020-04-12 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200412_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitemaddon',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
