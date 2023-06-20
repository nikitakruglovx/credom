from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    uu_id = models.CharField(max_length=50, primary_key=True)
    wallet_address = models.CharField(max_length=45, null=True)
    seed = models.CharField(max_length=100, null=True)
    privatekey = models.CharField(max_length=100, null=True)
    who_member = models.CharField(max_length=60, null=True, blank=True)
    avatar_profile = models.ImageField(default='avatar/person.png', upload_to='avatar/', null=True, blank=True)
    background_profile = models.ImageField(default='avatarback/cover.png', upload_to='avatarback/', null=True, blank=True)

    def __str__(self):
        return str(self.username)

class CloudFiles(models.Model):
    author_files = models.ForeignKey(Users, related_name='author_files',on_delete=models.CASCADE, null=True)
    name_file = models.CharField(max_length=500, null=True)
    total_size = models.CharField(max_length=100, null=True)
    folder = models.ForeignKey('Folder', null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/CloudFiles/', null=True)
    datatime = models.DateTimeField(verbose_name='Date and Time', auto_now_add=True, null=True)

    class Meta:
        ordering = ["-datatime"]

    def __str__(self):
        return str(self.name_file)

class Folder(models.Model):
     folder = models.CharField(max_length=30, verbose_name='Название диска')
     password_folder = models.CharField(max_length=50, null=True)
     author_folder = models.ForeignKey(Users, on_delete=models.CASCADE)
    
     def __str__(self):
         return self.folder

class Items(models.Model):
    SITESANDWEB = 'sitesandweb'
    SCRIPTS = 'scripts'
    BOTS = 'bots'
    ANDROIDAPP = 'androidapp'
    DESKTOPSOFT = 'desktopsoft'
    FRONTENDTAMPLATE = 'frontendtamplate'
    LOGOTYPE = 'logotype'
    TREEDMODELS = 'treedmodels'
    BOOKS = 'books'
    COURSES = 'courses'


    GROUP = {
        (SITESANDWEB, 'Сайты/Веб-приложения'),
        (SCRIPTS, 'Скрипты'),
        (BOTS, 'Онлайн боты'),
        (ANDROIDAPP, 'Мобильные приложения для Android'),
        (DESKTOPSOFT, 'Десктоп софт'),
        (FRONTENDTAMPLATE, 'html/css/js Frontend Шаблоны'),
        (LOGOTYPE, 'Логотипы'),
        (TREEDMODELS, '3D модели'),
        (BOOKS, 'Электронные книги'),
        (COURSES, 'Обучающие курсы'),
        
    }
    author = models.ForeignKey(Users, related_name='author',on_delete=models.CASCADE, null=True)
    photo_item = models.ImageField(upload_to='media/', null=True)
    two_photo_item = models.ImageField(upload_to='media/', null=True, blank=True)
    tree_photo_item = models.ImageField(upload_to='media/', null=True, blank=True)
    four_photo_item = models.ImageField(upload_to='media/', null=True, blank=True)
    name_item = models.CharField(max_length=200)
    text_item = models.TextField(max_length=5000, null=True)
    price_item = models.FloatField(null=True)
    choice_group = models.CharField(max_length=50, choices=GROUP, default=SITESANDWEB)
    archive_file = models.FileField(upload_to='media/files/', null=True, blank=True)
    file_link = models.CharField(max_length=500, null=True, blank=True)
    datatime = models.DateTimeField(verbose_name='Date and Time', auto_now_add=True, null=True)
    orders_buyers = models.ManyToManyField(Users)

    class Meta:
        ordering = ["-datatime"]
    
    def __str__(self):
        return str(self.name_item)

class News(models.Model):
    title = models.CharField(null=True, max_length=500)
    text = models.CharField(null=True, max_length=1000)
    datatime = models.DateTimeField(verbose_name='Date and Time', auto_now_add=True, null=True)

    class Meta:
        ordering = ["-datatime"]



        