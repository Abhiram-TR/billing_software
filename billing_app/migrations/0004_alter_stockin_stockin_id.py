# Generated by Django 5.0.7 on 2024-07-18 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0003_remove_stockin_material_stockin_stockin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockin',
            name='stockin_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
