# Generated by Django 4.1 on 2022-08-04 11:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("banco_api", "0013_delete_fatura"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fatura",
            fields=[
                ("fatura_id", models.AutoField(primary_key=True, serialize=False)),
                ("data_abertura", models.DateTimeField(default=datetime.datetime.now)),
                ("data_vencimento", models.DateTimeField()),
                ("data_pagamento", models.DateTimeField(null=True)),
                (
                    "valor",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                ("status_pagamento", models.BooleanField(default=False)),
                (
                    "cliente",
                    models.ForeignKey(
                        db_column="conta",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="banco_api.conta",
                    ),
                ),
            ],
            options={
                "db_table": "faturas",
            },
        ),
    ]