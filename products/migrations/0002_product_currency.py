# Generated by Django 3.2.15 on 2022-10-30 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(choices=[('UAH', 'UAH'), ('USD', 'USD'), ('EUR', 'EUR')], default='UAH', max_length=3),
        ),
    ]
