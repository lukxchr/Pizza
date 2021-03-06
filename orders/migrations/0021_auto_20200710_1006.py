# Generated by Django 2.2.6 on 2020-07-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Orders Dashboard',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('orders.order',),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_estimate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
