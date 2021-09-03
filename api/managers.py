from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        if username:
            user.username = username
        else:
            user.username = email
        user.save()
        return user

    def create_superuser(self, email, username=None, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.set_admin()
        if username:
            user.username = username
        else:
            user.username = email
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
