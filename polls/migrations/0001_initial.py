# Generated by Django 4.0.1 on 2022-04-12 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Baseuser',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('maxcontent', models.IntegerField(blank=True, null=True)),
                ('dailycontentmarked', models.IntegerField(blank=True, null=True)),
                ('maxmetdate', models.DateField(blank=True, null=True)),
                ('maxmet', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'baseuser',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('user_role', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=500)),
                ('identifier', models.CharField(max_length=300)),
                ('reason', models.CharField(max_length=300)),
                ('placeholder', models.CharField(max_length=300)),
                ('isblocked', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'content',
            },
        ),
        migrations.CreateModel(
            name='Priviligeduser',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('user_role', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'priviligeduser',
            },
        ),
        migrations.CreateModel(
            name='Reportrequest',
            fields=[
                ('r_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('user_role', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=500)),
                ('identifier', models.CharField(max_length=300)),
                ('reason', models.CharField(max_length=300)),
                ('placeholder', models.CharField(max_length=300)),
                ('isresolved', models.BooleanField(blank=True, null=True)),
                ('baseuserid', models.OneToOneField(blank=True, db_column='userid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.baseuser')),
                ('c', models.OneToOneField(blank=True, db_column='c_id', db_index=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.content')),
                ('priviligeduserid', models.ForeignKey(blank=True, db_column='priviligeduserid', db_index=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.priviligeduser')),
            ],
            options={
                'db_table': 'reportrequest',
            },
        ),
        migrations.CreateModel(
            name='Createrequest',
            fields=[
                ('r_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('user_role', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=500)),
                ('identifier', models.CharField(max_length=300)),
                ('reason', models.CharField(max_length=300)),
                ('placeholder', models.CharField(max_length=300)),
                ('isresolved', models.BooleanField(blank=True, null=True)),
                ('baseuserid', models.OneToOneField(blank=True, db_column='userid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.baseuser')),
                ('priviligeduserid', models.ForeignKey(blank=True, db_column='priviligeduserid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.priviligeduser')),
            ],
            options={
                'db_table': 'createrequest',
            },
        ),
        migrations.AddField(
            model_name='content',
            name='create_r',
            field=models.OneToOneField(blank=True, db_column='r_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.createrequest'),
        ),
        migrations.AddField(
            model_name='content',
            name='priviligeduserid',
            field=models.OneToOneField(blank=True, db_column='priviligeduserid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.priviligeduser'),
        ),
    ]
