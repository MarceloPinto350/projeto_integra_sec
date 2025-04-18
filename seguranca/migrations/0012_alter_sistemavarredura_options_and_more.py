# Generated by Django 4.2.13 on 2024-07-03 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seguranca', '0011_alter_versaoaplicacao_data_lancamento_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sistemavarredura',
            options={'ordering': ['nome'], 'permissions': [('can_view_sistema_varredura', 'Can view sistemas varredura'), ('can_change_sistema_varredura', 'Can change sistemas varredura'), ('can_add_sistema_varredura', 'Can add sistemas varredura'), ('can_delete_sistema_varredura', 'Can delete sistemas varredura')], 'verbose_name': 'Sistema de Varredura', 'verbose_name_plural': 'Sistemas de Varredura'},
        ),
        migrations.RemoveField(
            model_name='sistemavarredura',
            name='tipo',
        ),
    ]
