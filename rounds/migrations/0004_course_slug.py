# Generated by Django 4.2.1 on 2023-06-04 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rounds', '0003_remove_hole_course_holedisplay'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(default='Maplewood', unique=True),
            preserve_default=False,
        ),
    ]
