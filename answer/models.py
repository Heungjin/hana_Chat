# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Banks(models.Model):
    bank_id = models.IntegerField(primary_key=True)
    bank_name = models.CharField(max_length=20, blank=True, null=True)
    bank_image = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'banks'


class CustomerInfo(models.Model):
    cus_num = models.AutoField(primary_key=True)
    cus_age = models.IntegerField(blank=True, null=True)
    cus_sex = models.IntegerField(blank=True, null=True)
    repayment = models.IntegerField(blank=True, null=True)
    repayment_money = models.FloatField(blank=True, null=True)
    cus_salary = models.FloatField(blank=True, null=True)
    cus_loan = models.FloatField(blank=True, null=True)
    leasing_mortgage = models.FloatField(blank=True, null=True)
    month_loan_period = models.IntegerField(blank=True, null=True)
    bank_id = models.IntegerField(blank=True, null=True)
    input_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_info'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LoanGoods(models.Model):
    loan_num = models.IntegerField(primary_key=True)
    loan_good_name = models.CharField(max_length=50, blank=True, null=True)
    loan_bank = models.ForeignKey(Banks, models.DO_NOTHING, blank=True, null=True)
    avg_int_rat = models.FloatField(blank=True, null=True)
    money_credit_line = models.FloatField(blank=True, null=True)
    rate_credit_line = models.FloatField(blank=True, null=True)
    salary_credit_line = models.FloatField(blank=True, null=True)
    month_loan_period_line = models.IntegerField(blank=True, null=True)
    loan_repayment = models.IntegerField(blank=True, null=True)
    loan_url = models.CharField(max_length=200, blank=True, null=True)
    loan_img = models.CharField(max_length=50, blank=True, null=True)
    num_recommend = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan_goods'


class TbCalc(models.Model):
    calc_num = models.AutoField(primary_key=True)
    calc_cus_num = models.ForeignKey(CustomerInfo, models.DO_NOTHING, db_column='calc_cus_num', blank=True, null=True)
    calc_loan_num = models.ForeignKey(LoanGoods, models.DO_NOTHING, db_column='calc_loan_num', blank=True, null=True)
    like_loan = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_calc'


class TbCalc2(models.Model):
    calc2_cus_num = models.ForeignKey(CustomerInfo, models.DO_NOTHING, db_column='calc2_cus_num', blank=True, null=True)
    calc2_loan_num = models.ForeignKey(LoanGoods, models.DO_NOTHING, db_column='calc2_loan_num', blank=True, null=True)
    select_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_calc2'
