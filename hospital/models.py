# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Diagnosis(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='NAME')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'DIAGNOSIS'


class Doctor(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='NAME')  # Field name made lowercase. This field type is a guess.
    surname = models.TextField(db_column='SURNAME')  # Field name made lowercase. This field type is a guess.
    department = models.TextField(db_column='DEPARTMENT')  # Field name made lowercase. This field type is a guess.
    title = models.TextField(db_column='TITLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    email = models.TextField(db_column='EMAIL', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    phone = models.TextField(db_column='PHONE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    salary = models.TextField(db_column='SALARY', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    off_day = models.TextField(db_column='OFF_DAY', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'DOCTOR'


class Patient(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='NAME')  # Field name made lowercase. This field type is a guess.
    surname = models.TextField(db_column='SURNAME')  # Field name made lowercase. This field type is a guess.
    gender = models.TextField(db_column='GENDER', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    birthdate = models.DateField(db_column='BIRTHDATE', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='EMAIL', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    phone = models.TextField(db_column='PHONE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'PATIENT'


class Service(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='NAME')  # Field name made lowercase. This field type is a guess.
    unit_price = models.TextField(db_column='UNIT_PRICE')  # Field name made lowercase. This field type is a guess.
    quantity = models.IntegerField(db_column='QUANTITY')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SERVICE'


class Visit(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='DOCTOR_ID')  # Field name made lowercase.
    patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='PATIENT_ID')  # Field name made lowercase.
    type = models.TextField(db_column='TYPE')  # Field name made lowercase. This field type is a guess.
    date = models.DateField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='STATE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VISIT'


class VisitProcess(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    visit = models.ForeignKey(Visit, models.DO_NOTHING, db_column='VISIT_ID')  # Field name made lowercase.
    service = models.ForeignKey(Service, models.DO_NOTHING, db_column='SERVICE_ID')  # Field name made lowercase.
    diagnosis = models.ForeignKey(Diagnosis, models.DO_NOTHING, db_column='DIAGNOSIS_ID')  # Field name made lowercase.
    process_date = models.DateField(db_column='PROCESS_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VISIT_PROCESS'
