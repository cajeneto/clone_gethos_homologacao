# Generated by Django 5.1.1 on 2025-03-30 18:15

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contato",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                ("telefone", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("empresa", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Lead", "Lead"),
                            ("Cliente Ativo", "Cliente Ativo"),
                            ("Inativo", "Inativo"),
                        ],
                        default="Lead",
                        max_length=20,
                    ),
                ),
                ("observacoes", models.TextField(blank=True, null=True)),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "whatsapp",
                    models.CharField(
                        blank=True,
                        help_text="Número de WhatsApp no formato +5582987654321",
                        max_length=15,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\+55\\d{10,11}$",
                                "Digite o número de WhatsApp no formato +5582987654321 (com código do país +55 e 10 ou 11 dígitos).",
                            )
                        ],
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Campanha",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                ("mensagem", models.TextField()),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("WhatsApp", "WhatsApp"),
                            ("Email", "E-mail"),
                            ("Ambos", "Ambos"),
                        ],
                        default="WhatsApp",
                        max_length=20,
                    ),
                ),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pendente", "Pendente"),
                            ("Enviando", "Enviando"),
                            ("Concluída", "Concluída"),
                        ],
                        default="Pendente",
                        max_length=20,
                    ),
                ),
                (
                    "contatos",
                    models.ManyToManyField(
                        related_name="campanhas", to="gethos_home.contato"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MensagemWhatsApp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[("WhatsApp", "WhatsApp"), ("Email", "E-mail")],
                        default="WhatsApp",
                        max_length=20,
                    ),
                ),
                ("mensagem", models.TextField()),
                ("data_envio", models.DateTimeField(blank=True, null=True)),
                ("enviado", models.BooleanField(default=False)),
                (
                    "campanha",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gethos_home.campanha",
                    ),
                ),
                (
                    "contato",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mensagem_whatsapp_gethos_home",
                        to="gethos_home.contato",
                    ),
                ),
            ],
        ),
    ]
