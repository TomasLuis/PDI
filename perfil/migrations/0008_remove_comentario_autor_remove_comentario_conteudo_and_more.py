# Generated by Django 5.1.7 on 2025-05-03 16:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0007_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='conteudo',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='data',
        ),
        migrations.AddField(
            model_name='comentario',
            name='comentario',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='comentario',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='comentario',
            name='nome_utilizador',
            field=models.CharField(default='', max_length=255),
        ),
    ]
