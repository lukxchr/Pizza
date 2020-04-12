# Generated by Django 2.0.3 on 2020-04-11 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_auto_20200410_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Placed', 'Placed'), ('Making', 'Making'), ('Delivery', 'On the Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Extra')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPizzaTopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_topping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.PizzaTopping')),
                ('order_pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toppings', to='orders.OrderPizza')),
            ],
        ),
        migrations.CreateModel(
            name='StandardMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Sub', 'Sub'), ('SubExtra', 'SubExtra'), ('Pasta', 'Pasta'), ('Platter', 'DinnerPlatter')], default='Sub', max_length=15)),
                ('name', models.CharField(max_length=64)),
                ('size', models.CharField(blank=True, choices=[('S', 'Small'), ('L', 'Large')], max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='StandardOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.StandardMenuItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standard_items', to='orders.Order')),
            ],
        ),
        migrations.DeleteModel(
            name='DinnerPlatter',
        ),
        migrations.DeleteModel(
            name='Pasta',
        ),
        migrations.DeleteModel(
            name='Sub',
        ),
        migrations.DeleteModel(
            name='SubExtra',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='price',
        ),
        migrations.AddField(
            model_name='pizza',
            name='crust',
            field=models.CharField(choices=[('Regular', 'Regular'), ('Sicilian', 'Sicilian')], default='Regular', max_length=8),
        ),
        migrations.AddField(
            model_name='orderpizza',
            name='menu_pizza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Pizza'),
        ),
        migrations.AddField(
            model_name='orderpizza',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizzas', to='orders.Order'),
        ),
        migrations.AddField(
            model_name='orderextra',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extras', to='orders.StandardOrderItem'),
        ),
    ]
