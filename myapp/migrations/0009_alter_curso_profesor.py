# Generated by Django 4.2.2 on 2023-06-14 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_curso_profesor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data', to='myapp.profesor'),
        ),
    ]