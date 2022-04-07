# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


# Create your models here.
