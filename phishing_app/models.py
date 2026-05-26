from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    # class Meta:
    #     db_table = "users"  # Match your MySQL table name