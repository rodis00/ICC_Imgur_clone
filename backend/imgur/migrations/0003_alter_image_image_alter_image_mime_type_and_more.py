# Generated by Django 4.1.7 on 2023-03-29 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imgur', '0002_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='mime_type',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='path',
            field=models.CharField(max_length=90, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='imgur.post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='size',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
