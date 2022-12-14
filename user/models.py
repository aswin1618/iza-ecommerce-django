from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountMananger(BaseUserManager):
    def create_user(self,first_name,last_name,username, email,password= None):
        if not email:
            raise ValueError('user must have an email')

        if not username:
            raise ValueError('user must have username')
        

        user =self.model(
            email = self.normalize_email(email),
            username = username,
            first_name =first_name,
            last_name =last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email ,username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name =first_name,
            last_name =last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser,):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique= True)
    email = models.CharField(max_length=50 , unique = True)
    phone_number = models.CharField(max_length=50)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountMananger()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self ,add_label ):
        return True
   
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')

    
    def __str__(self):
        return self.user.first_name
 
    
class UserAdress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=15,null=True)
    adress_line_1 = models.CharField(blank=True,max_length=100)
    adress_line_2 = models.CharField(blank=True,max_length=100)
    pin_code = models.IntegerField(null=True)
    district = models.CharField(max_length=20,null=True)
    city = models.CharField(blank=True,max_length=20)
    state = models.CharField(blank=True,max_length=20)
    

    def __str__(self):
        return f'{self.adress_line_1} {self.adress_line_2} {self.city} {self.state}'
    
    def snap(self):
        return f'{self.user}, {self.adress_line_1}, {self.adress_line_2}.....'

   
