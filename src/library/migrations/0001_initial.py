# Generated by Django 4.0.2 on 2022-02-17 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('identity_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BookItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISBN', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('language', models.CharField(choices=[('English', 'English'), ('French', 'French'), ('German', 'German'), ('Spanish', 'Spanish')], max_length=200)),
                ('numOfPages', models.IntegerField()),
                ('barcode', models.CharField(max_length=500)),
                ('isReferenceOnly', models.BooleanField(default=False)),
                ('borrowed', models.DateField()),
                ('dueDate', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('status', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=100)),
                ('datePurchase', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BookLending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateField(auto_now_add=True)),
                ('dueDate', models.DateField()),
                ('returnedDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('locationIdentifier', models.CharField(max_length=150)),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.library')),
            ],
        ),
        migrations.CreateModel(
            name='BookReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateField(auto_now_add=True)),
                ('reservationStatus', models.CharField(max_length=100)),
                ('bookItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bookitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='identity_manager.account')),
            ],
        ),
        migrations.AddField(
            model_name='bookitem',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.library'),
        ),
        migrations.AddField(
            model_name='bookitem',
            name='rack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.rack'),
        ),
    ]