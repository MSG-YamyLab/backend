from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Fields email must be required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
     
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        
        if not kwargs.get('is_superuser'):
            raise ValueError('Fields Superuser is not True')

        if not kwargs.get('is_staff'):
            raise ValueError('Fields Staff is not True')

        user = self.create_user(email, password, **kwargs)
        return user
