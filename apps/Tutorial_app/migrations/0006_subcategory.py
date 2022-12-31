# Generated by Django 4.1 on 2022-08-15 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutorial_app', '0005_videotutorial_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(related_name='subcategory', to='Tutorial_app.category')),
            ],
        ),
    ]