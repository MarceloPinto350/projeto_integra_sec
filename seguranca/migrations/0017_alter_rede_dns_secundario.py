# Generated by Django 4.2.13 on 2024-07-16 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguranca', '0016_modelodocumento_arquivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rede',
            name='dns_secundario',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='IPv4', verbose_name='DNS Secundário'),
        ),
    ]
