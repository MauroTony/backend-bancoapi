# Generated by Django 4.1 on 2022-08-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banco_api", "0009_fatura_data_abertura_alter_fatura_data_pagamento_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fatura",
            name="valor",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]