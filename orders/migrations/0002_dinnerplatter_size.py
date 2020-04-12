# Generated by Django 2.0.3 on 2020-04-10 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinnerplatter',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('L', 'Large')], default='L', max_length=1),
        ),
    ]
