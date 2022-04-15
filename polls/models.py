# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.utils import timezone
import datetime

class Account(models.Model):
    userid = models.AutoField(primary_key = True, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=50)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

class Priviligeduser(Account):
    user_role = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'priviligeduser'

#class Admin(Account):
    #priviligeduserid = models.OneToOneField(Priviligeduser, models.DO_NOTHING, db_column='priviligeduserid', blank=True, null=True)
    #class Meta:
        #db_table = 'admin'

#class Moderator(Account):
    #priviligeduserid = models.OneToOneField(Priviligeduser, models.DO_NOTHING, db_column='priviligeduserid', blank=True, null=True)
    #class Meta:
        #db_table = 'moderator'
class Baseuser(Account):
    maxcontent = models.IntegerField(blank=True, null=True)
    dailycontentmarked = models.IntegerField(blank=True, null=True)
    maxmetdate = models.DateTimeField(blank=True, null=True)
    maxmet = models.BooleanField(blank=True, null=True)
    def reset_limit(self):
        return self.maxmetdate <= timezone.now() - datetime.timedelta(days=1) and self.maxmet==True

    class Meta:
        db_table = 'baseuser'



class Request(models.Model):
    r_id = models.AutoField(primary_key=True, unique = True)
    baseuserid = models.ForeignKey(Baseuser, models.DO_NOTHING, db_column='baseuserid', blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now=True)
    user_role = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    identifier = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=300)
    isresolved = models.BooleanField(blank=True, null=True)

    class Meta:
        abstract = True

class Createrequest(Request):
    priviligeduserid = models.ForeignKey('Priviligeduser', models.DO_NOTHING,  db_column='priviligeduserid', blank=True, null=True)

    class Meta:
        db_table = 'createrequest'


class Content(models.Model):
    c_id = models.AutoField(primary_key=True, unique = True)
    priviligeduserid = models.OneToOneField('Priviligeduser', models.DO_NOTHING,  db_column='priviligeduserid', blank=True, null=True)
    create_r_id = models.OneToOneField('Createrequest', models.DO_NOTHING, db_column='create_r_id', blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now=True)
    user_role = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    identifier = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=300)
    isblocked = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'content'

class Reportrequest(Request):
    c = models.OneToOneField(Content, models.DO_NOTHING, db_column='c_id', db_index=False, blank=True, null=True)
    priviligeduserid = models.ForeignKey(Priviligeduser, models.DO_NOTHING, db_index=False, db_column='priviligeduserid', blank=True, null=True)

    class Meta:
        db_table = 'reportrequest'



