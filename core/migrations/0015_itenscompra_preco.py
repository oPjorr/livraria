# Generated by Django 5.1.3 on 2024-12-19 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_compra_itenscompra"),
    ]

    operations = [
        migrations.AddField(
            model_name="itenscompra",
            name="preco",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
