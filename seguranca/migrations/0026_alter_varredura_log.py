# Generated by Django 4.2.13 on 2025-01-26 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguranca', '0025_remove_rede_ativo_infraestrutura_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='varredura',
            name='log',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Log'),
        ),
    ]
