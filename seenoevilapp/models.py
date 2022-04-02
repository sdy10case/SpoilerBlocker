# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    userid = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'account'


class Admin(models.Model):
    userid = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'admin'


class Baseuser(models.Model):
    userid = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    maxcontent = models.IntegerField(blank=True, null=True)
    dailycontentmarked = models.IntegerField(blank=True, null=True)
    maxmet = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'baseuser'


class Content(models.Model):
    c_id = models.AutoField(primary_key=True)
    priviligeduserid = models.ForeignKey('Priviligeduser', models.DO_NOTHING, db_column='priviligeduserid', blank=True, null=True)
    create_r = models.ForeignKey('Createrequest', models.DO_NOTHING, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    user_role = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    identifier = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=300)
    isblocked = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'content'


class Createrequest(models.Model):
    r_id = models.AutoField(primary_key=True)
    baseuserid = models.CharField(max_length=30, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    user_role = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    identifier = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=300)
    isresolved = models.BooleanField(blank=True, null=True)
    priviligeduserid = models.ForeignKey('Priviligeduser', models.DO_NOTHING, db_column='priviligeduserid', blank=True, null=True)

    class Meta:
        db_table = 'createrequest'


class Moderator(models.Model):
    userid = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'moderator'


class Priviligeduser(models.Model):
    userid = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'priviligeduser'


class Reportrequest(models.Model):
    r_id = models.AutoField(primary_key=True)
    baseuserid = models.CharField(max_length=30, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    user_role = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    identifier = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=300)
    isresolved = models.BooleanField(blank=True, null=True)
    c = models.OneToOneField(Content, models.DO_NOTHING)
    priviligeduserid = models.ForeignKey(Priviligeduser, models.DO_NOTHING, db_column='priviligeduserid', blank=True, null=True)

    class Meta:
        db_table = 'reportrequest'


class Request(models.Model):
    r_id = models.AutoField(primary_key=True)
    baseuserid = models.ForeignKey(Baseuser, models.DO_NOTHING, db_column='baseuserid', blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    user_role = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    identifier = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=300)
    isresolved = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'request'
