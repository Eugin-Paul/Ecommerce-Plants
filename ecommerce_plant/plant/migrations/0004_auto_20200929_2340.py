# Generated by Django 3.0.7 on 2020-09-29 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0003_auto_20200929_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='billing_address',
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plant.BillingAddress'),
        ),
    ]
