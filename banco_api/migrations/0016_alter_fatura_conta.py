# Generated by Django 4.1 on 2022-08-04 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banco_api", "0015_rename_cliente_fatura_conta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fatura",
            name="conta",
            field=models.IntegerField(unique=True),
        ),
    ]
