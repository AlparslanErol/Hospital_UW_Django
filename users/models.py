from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    usernumber = models.CharField(max_length=4)
    password = models.CharField(max_length=12)

    """
    The following methods are used to set if user has been logged into the system and what is the type of user.
    """
    def is_doctor(self):
        if self.usernumber.startswith('1'):
            return True
        else:
            return False

    def is_patient(self):
        if self.usernumber.startswith('2'):
            return True
        else:
            return False

    def is_admin(self):
        if self.usernumber.startswith('0'):
            return True
        else:
            return False

    def is_not_logged(self):
        if not(self.is_patient() or self.is_doctor() or self.is_admin()):
            return True
        else:
            return False

    def __str__(self):
        return self.name + " " + self.surname
