# Generated by Django 4.2.13 on 2024-11-03 17:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('seguranca', '0019_remove_aplicacao_bancos_dados_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoConfiguracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(max_length=500, verbose_name='Descrição')),
                ('tipo_arquivo', models.CharField(choices=[['JSON', 'JSON'], ['YAML', 'YAML'], ['XML', 'XML'], ['CSV', 'CSV'], ['XLS', 'XLS'], ['XLSX', 'XLSX'], ['DOC', 'DOC'], ['DOCX', 'DOCX'], ['PDF', 'PDF'], ['TXT', 'TXT'], ['ODF', 'ODF'], ['ODS', 'ODS'], ['OUTRO', 'Outro']], default='JSON', max_length=20, verbose_name='Tipo de Arquivo')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data Cadastro')),
                ('data_modificacao', models.DateTimeField(auto_now=True, verbose_name='Data Modificação')),
                ('arquivo', models.TextField(max_length=3000, verbose_name='Arquivo')),
            ],
            options={
                'verbose_name': 'Arquivo de Configuração',
                'verbose_name_plural': 'Arquivos de Configuração',
                'db_table': 'tb_arquivo_configuracao',
                'ordering': ['configuracao', 'descricao'],
                'permissions': [('can_view_arquivo_configuracao', 'Can view arquivos configuração'), ('can_change_arquivo_configuracao', 'Can change arquivos configuração'), ('can_add_arquivo_configuracao', 'Can add arquivos configuração'), ('can_delete_arquivo_configuracao', 'Can delete arquivos configuração')],
            },
        ),
        migrations.CreateModel(
            name='Configuracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(max_length=1000, verbose_name='Descrição')),
                ('ambiente', models.CharField(choices=[['PRODUÇÃO', 'Produção'], ['HOMOLOGAÇÃO', 'Homologação'], ['DESENVOLVIMENTO', 'Desenvolvimento'], ['TESTE', 'Teste'], ['TREINAMENTO', 'Treinamento'], ['OUTRO', 'Outro']], default='DESENVOLVIMENTO', max_length=50, verbose_name='Ambiente')),
                ('url_acesso', models.URLField(verbose_name='URL de acesso à aplicação')),
                ('senha_servico', models.CharField(max_length=50, verbose_name='Senha de serviço')),
                ('token_acesso', models.CharField(max_length=1000, verbose_name='Token de acesso')),
            ],
            options={
                'verbose_name': 'Configuração',
                'verbose_name_plural': 'Configurações',
                'db_table': 'tb_configuracao',
                'permissions': [('can_view_configuracao', 'Can view configurações'), ('can_change_configuracao', 'Can change configurações'), ('can_add_configuracao', 'Can add configurações'), ('can_delete_configuracao', 'Can delete configurações')],
            },
        ),
        migrations.CreateModel(
            name='Relacionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Relacionamento',
                'verbose_name_plural': 'Relacionamentos',
                'db_table': 'tb_relacionamento',
                'permissions': [('can_view_relacionamento', 'Can view relacionamentos'), ('can_change_relacionamento', 'Can change relacionamentos'), ('can_add_relacionamento', 'Can add relacionamentos'), ('can_delete_relacionamento', 'Can delete relacionamentos')],
            },
        ),
        migrations.CreateModel(
            name='TipoRelacionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(max_length=1000, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Tipo de Relacionamento',
                'verbose_name_plural': 'Tipos de Relacionamento',
                'db_table': 'tb_tipo_relacionamento',
                'ordering': ['nome'],
                'permissions': [('can_view_tipo_relacionamento', 'Can view tipos relacionamento'), ('can_change_tipo_relacionamento', 'Can change tipos relacionamento'), ('can_add_tipo_relacionamento', 'Can add tipos relacionamento'), ('can_delete_tipo_relacionamento', 'Can delete tipos relacionamento')],
            },
        ),
        migrations.CreateModel(
            name='Varredura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origem', models.CharField(max_length=100, verbose_name='Origem')),
                ('data_inicio', models.DateTimeField(verbose_name='Data Início')),
                ('data_fim', models.DateTimeField(verbose_name='Data Fim')),
                ('vulnerabilidades', models.IntegerField(default=0, verbose_name='Vulnerabilidades')),
                ('erros', models.IntegerField(default=0, verbose_name='Erros')),
                ('situacao', models.CharField(choices=[['EM ANDAMENTO', 'Em andamento'], ['CONCLUÍDA', 'Concluída'], ['FALHA', 'Falha']], max_length=20, verbose_name='Situação')),
                ('log', models.FileField(blank=True, null=True, upload_to='logs/', verbose_name='Log')),
            ],
            options={
                'verbose_name': 'Varredura',
                'verbose_name_plural': 'Varreduras',
                'db_table': 'tb_varredura',
                'ordering': ['aplicacao', '-data_inicio'],
                'permissions': [('can_view_varredura', 'Can view varreduras'), ('can_change_varredura', 'Can change varreduras'), ('can_add_varredura', 'Can add varreduras'), ('can_delete_varredura', 'Can delete varreduras')],
            },
        ),
        migrations.AlterModelOptions(
            name='ativoinfraestrutura',
            options={'ordering': ['tipo_ativo', 'nome'], 'permissions': [('can_view_ativo_infraestrutura', 'Can view ativos infraestrutura'), ('can_change_ativo_infraestrutura', 'Can change ativos infraestrutura'), ('can_add_ativo_infraestrutura', 'Can add ativos infraestrutura'), ('can_delete_ativo_infraestrutura', 'Can delete ativos infraestrutura')], 'verbose_name': 'Ativo de Infraestrutura', 'verbose_name_plural': 'Ativos de Infraestrutura'},
        ),
        migrations.AlterModelOptions(
            name='bancodados',
            options={'ordering': ['tipo'], 'permissions': [('can_view_banco_dados', 'Can view bancos dados'), ('can_change_banco_dados', 'Can change bancos dados'), ('can_add_banco_dados', 'Can add bancos dados'), ('can_delete_banco_dados', 'Can delete bancos dados')], 'verbose_name': 'Banco de Dados', 'verbose_name_plural': 'Bancos de Dados'},
        ),
        migrations.AlterModelOptions(
            name='rede',
            options={'ordering': ['tipo'], 'permissions': [('can_view_rede', 'Can view redes'), ('can_change_rede', 'Can change redes'), ('can_add_rede', 'Can add redes'), ('can_delete_rede', 'Can delete redes')], 'verbose_name': 'Rede', 'verbose_name_plural': 'Redes'},
        ),
        migrations.AlterModelOptions(
            name='servico',
            options={'ordering': ['nome_servico'], 'permissions': [('can_view_servico', 'Can view serviços'), ('can_change_servico', 'Can change serviços'), ('can_add_servico', 'Can add serviços'), ('can_delete_servico', 'Can delete serviços')], 'verbose_name': 'Serviço', 'verbose_name_plural': 'Serviços'},
        ),
        migrations.AlterModelOptions(
            name='servidor',
            options={'ordering': ['tipo'], 'permissions': [('can_view_servidor', 'Can view servidores'), ('can_change_servidor', 'Can change servidores'), ('can_add_servidor', 'Can add servidores'), ('can_delete_servidor', 'Can delete servidores')], 'verbose_name': 'Servidor', 'verbose_name_plural': 'Servidores'},
        ),
        migrations.AlterModelOptions(
            name='sistemavarredura',
            options={'ordering': ['aplicacao_seguranca', 'tipo_varredura'], 'permissions': [('can_view_sistema_varredura', 'Can view sistemas varredura'), ('can_change_sistema_varredura', 'Can change sistemas varredura'), ('can_add_sistema_varredura', 'Can add sistemas varredura'), ('can_delete_sistema_varredura', 'Can delete sistemas varredura')], 'verbose_name': 'Sistema de Varredura', 'verbose_name_plural': 'Sistemas de Varredura'},
        ),
        migrations.RenameField(
            model_name='aplicacao',
            old_name='tipo',
            new_name='tipo_aplicacao',
        ),
        migrations.RenameField(
            model_name='aplicacao',
            old_name='url_fonte',
            new_name='url_codigo_fonte',
        ),
        migrations.RenameField(
            model_name='ativoinfraestrutura',
            old_name='status',
            new_name='situacao',
        ),
        migrations.RenameField(
            model_name='ativoinfraestrutura',
            old_name='tipo',
            new_name='tipo_ativo',
        ),
        migrations.RenameField(
            model_name='bancodados',
            old_name='ativo_infra_db',
            new_name='ativo_infraestrutura',
        ),
        migrations.RenameField(
            model_name='servico',
            old_name='ativo_infra_svc',
            new_name='ativo_infraestrutura',
        ),
        migrations.RenameField(
            model_name='sistemavarredura',
            old_name='status',
            new_name='situacao',
        ),
        migrations.RemoveField(
            model_name='aplicacao',
            name='ativo_infra_app',
        ),
        migrations.RemoveField(
            model_name='aplicacao',
            name='senha_servico',
        ),
        migrations.RemoveField(
            model_name='aplicacao',
            name='token_acesso',
        ),
        migrations.RemoveField(
            model_name='aplicacao',
            name='url_acesso',
        ),
        migrations.RemoveField(
            model_name='ativoinfraestrutura',
            name='endereco_ip',
        ),
        migrations.RemoveField(
            model_name='ativoinfraestrutura',
            name='porta_acesso',
        ),
        migrations.RemoveField(
            model_name='ativoinfraestrutura',
            name='senha_acesso',
        ),
        migrations.RemoveField(
            model_name='ativoinfraestrutura',
            name='token_acesso',
        ),
        migrations.RemoveField(
            model_name='ativoinfraestrutura',
            name='url_localizacao',
        ),
        migrations.RemoveField(
            model_name='ativoinfraestrutura',
            name='usuario_acesso',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='data_cadastro',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='data_modificacao',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='porta',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='servidor',
        ),
        migrations.RemoveField(
            model_name='bancodados',
            name='status',
        ),
        migrations.RemoveField(
            model_name='modelodocumento',
            name='arquivo',
        ),
        migrations.RemoveField(
            model_name='modelodocumento',
            name='ativa',
        ),
        migrations.RemoveField(
            model_name='modelodocumento',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='data_cadastro',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='data_modificacao',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='dns_primario',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='dns_secundario',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='servidores',
        ),
        migrations.RemoveField(
            model_name='rede',
            name='status',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='aplicacoes',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='data_cadastro',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='data_modificacao',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='status',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='ativo_infra_srv',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='data_cadastro',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='data_modificacao',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='servidor',
            name='status',
        ),
        migrations.RemoveField(
            model_name='sistemavarredura',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='sistemavarredura',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='sistemavarredura',
            name='tipos_varreduras',
        ),
        migrations.RemoveField(
            model_name='sistemavarredura',
            name='url',
        ),
        migrations.RemoveField(
            model_name='versaoaplicacao',
            name='bancos_dados',
        ),
        migrations.RemoveField(
            model_name='versaoaplicacao',
            name='servicos',
        ),
        migrations.RemoveField(
            model_name='versaoaplicacao',
            name='servidores',
        ),
        migrations.RemoveField(
            model_name='versaoaplicacao',
            name='sistema_varreduras',
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='abrangencia',
            field=models.TextField(choices=[['REGIONAL', 'Regional'], ['NACIONAL', 'Nacional'], ['CNJ', 'CNJ']], default='REGIONAL', verbose_name='Abrangência'),
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='essencial',
            field=models.BooleanField(default=True, verbose_name='Essencial'),
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='estrategica',
            field=models.BooleanField(default=False, verbose_name='Estratégica'),
        ),
        migrations.AddField(
            model_name='ativoinfraestrutura',
            name='data_cadastro',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data Cadastro'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ativoinfraestrutura',
            name='data_modificacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data Modificação'),
        ),
        migrations.AddField(
            model_name='bancodados',
            name='string_conexao',
            field=models.TextField(default=0, max_length=1000, verbose_name='String de Conexão'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bancodados',
            name='versao',
            field=models.TextField(default=django.utils.timezone.now, max_length=50, verbose_name='Versão'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modelodocumento',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='modelodocumento',
            name='modelo',
            field=models.TextField(default=django.utils.timezone.now, max_length=3000, verbose_name='Modelo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modelodocumento',
            name='tipo_modelo',
            field=models.CharField(choices=[['POD', 'POD'], ['SERVICES', 'Services'], ['INGRESS', 'Ingress'], ['CONFIGMAP', 'ConfigMap'], ['SECRET', 'Secret'], ['PERSISTENT_VOLUME', 'Persistent Volume'], ['PERSISTENT_VOLUME_CLAIM', 'Persistent Volume Claim'], ['STATEFUL_SET', 'Stateful Set'], ['DEPLOYMENT', 'Deployment'], ['JOB', 'Job'], ['CRONJOB', 'CronJob'], ['SERVICE_ACCOUNT', 'Service Account'], ['ROLE', 'Role'], ['ROLE_BINDING', 'Role Binding'], ['CLUSTER_ROLE', 'Cluster Role'], ['CLUSTER_ROLE_BINDING', 'Cluster Role Binding'], ['NETWORK_POLICY', 'Network Policy'], ['POD_SECURITY_POLICY', 'Pod Security Policy'], ['CUSTOM_RESOURCE_DEFINITION', 'Custom Resource Definition'], ['OUTRO', 'Outro']], default='OUTRO', max_length=50, verbose_name='Tipo Modelo de Documento'),
        ),
        migrations.AddField(
            model_name='rede',
            name='ativo_infraestrutura',
            #field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='seguranca.ativoinfraestrutura', verbose_name='Ativo de Infraestrutura'),
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='seguranca.ativoinfraestrutura', verbose_name='Ativo de Infraestrutura'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servico',
            name='nome_servico',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, unique=True, verbose_name='Nome do serviço'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servico',
            name='porta',
            #field=models.IntegerField(default=django.utils.timezone.now, verbose_name='Porta de serviço'),
            field=models.IntegerField(default=0, verbose_name='Porta de serviço'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servidor',
            name='bancos_dados',
            field=models.ManyToManyField(blank=True, related_name='servidores', to='seguranca.bancodados'),
        ),
        migrations.AddField(
            model_name='servidor',
            name='redes',
            field=models.ManyToManyField(blank=True, related_name='servidores', to='seguranca.rede'),
        ),
        migrations.AddField(
            model_name='sistemavarredura',
            name='aplicacao_seguranca',
            #field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='seguranca.aplicacao', verbose_name='Aplicação de Segurança'),
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='seguranca.aplicacao', verbose_name='Aplicação de Segurança'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sistemavarredura',
            name='comando',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000, verbose_name='Comando'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sistemavarredura',
            name='ip_acesso',
            #field=models.GenericIPAddressField(default=django.utils.timezone.now, protocol='IPv4', verbose_name='Endereço IP'),
            field=models.GenericIPAddressField(default='127.0.0.1', protocol='IPv4', verbose_name='Endereço IP'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sistemavarredura',
            name='tipo_varredura',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='seguranca.tipovarredura', verbose_name='Tipo de Varredura'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='versaoaplicacao',
            name='data_homologacao',
            field=models.DateField(blank=True, null=True, verbose_name='Data homologação'),
        ),
        migrations.AddField(
            model_name='versaoaplicacao',
            name='data_producao',
            field=models.DateField(blank=True, null=True, verbose_name='Data produção'),
        ),
        migrations.AlterField(
            model_name='modelodocumento',
            name='descricao',
            field=models.TextField(max_length=200, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='rede',
            name='tipo',
            field=models.CharField(choices=[['LAN', 'Local Area Network'], ['WAN', 'Wide Area Network'], ['WIFI', 'Rede sem fio'], ['VPN', 'Rede Privada Virtual'], ['DMZ', 'Zona Desmilitarizada']], default='LAN', max_length=50, verbose_name='Tipo de rede'),
        ),
        migrations.AlterField(
            model_name='resultadoscan',
            name='sistema_varredura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.sistemavarredura', verbose_name='Sistema de Varredura'),
        ),
        migrations.AlterField(
            model_name='servidor',
            name='servicos',
            field=models.ManyToManyField(blank=True, related_name='servidores', to='seguranca.servico'),
        ),
        migrations.AlterField(
            model_name='sistemavarredura',
            name='aplicacoes',
            field=models.ManyToManyField(blank=True, related_name='aplicacoes_varridas', to='seguranca.versaoaplicacao'),
        ),
        migrations.DeleteModel(
            name='TipoModeloDocumento',
        ),
        migrations.AddField(
            model_name='varredura',
            name='aplicacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.aplicacao', verbose_name='Aplicação'),
        ),
        migrations.AddField(
            model_name='relacionamento',
            name='aplicacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ativos_relacionados', to='seguranca.aplicacao'),
        ),
        migrations.AddField(
            model_name='relacionamento',
            name='ativo_infraestrutura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aplicacoes_relacionadas', to='seguranca.ativoinfraestrutura'),
        ),
        migrations.AddField(
            model_name='relacionamento',
            name='tipo_relacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.tiporelacionamento', verbose_name='Tipo de Relacionamento'),
        ),
        migrations.AddField(
            model_name='configuracao',
            name='ativo_infraestrutura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configuracoes', to='seguranca.ativoinfraestrutura'),
        ),
        migrations.AddField(
            model_name='configuracao',
            name='versao_aplicacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configuracoes', to='seguranca.versaoaplicacao'),
        ),
        migrations.AddField(
            model_name='arquivoconfiguracao',
            name='configuracao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.configuracao', verbose_name='Configuração'),
        ),
        migrations.AddField(
            model_name='arquivoconfiguracao',
            name='modelo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.modelodocumento', verbose_name='Modelo de Documento'),
        ),
        migrations.AddField(
            model_name='resultadoscan',
            name='varredura',
            #field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='seguranca.varredura', verbose_name='Varredura'),
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='seguranca.varredura', verbose_name='Varredura'),
            preserve_default=False,
        ),
    ]
