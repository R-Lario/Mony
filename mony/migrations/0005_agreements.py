# Generated by Django 4.1.3 on 2023-02-09 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mony', '0004_remove_banks_user_banks_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_id', models.CharField(max_length=64)),
                ('requisition_id', models.CharField(max_length=64)),
            ],
        ),
    ]
