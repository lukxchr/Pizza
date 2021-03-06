# Generated by Django 2.2.6 on 2020-05-27 09:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20200512_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='orders.Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_estimate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('CardOnline', 'Online by Card'), ('CashOnDelivery', 'Cash on Delivery'), ('CardOnDelivery', 'Card on Delivery')], default='CardOnline', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Placed', 'Placed'), ('Confirmed', 'Confirmed'), ('Making', 'Making'), ('Delivery', 'On the Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Placed', max_length=10),
        ),
    ]
