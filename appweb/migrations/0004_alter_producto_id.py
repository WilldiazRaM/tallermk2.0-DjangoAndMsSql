# Generated by Django 4.2.7 on 2024-01-23 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appweb', '0003_alter_producto_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]