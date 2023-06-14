from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=120, verbose_name='Имя проекта')
    descriptions = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/', verbose_name='Фотка')
    is_aproved = models.BooleanField(default=False, verbose_name='Отображать на сайте или нет')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = verbose_name + 'ы'

class Application(models.Model):
    name = models.CharField(max_length=127, verbose_name='Имя клиента')
    email = models.EmailField(verbose_name='Ваш емаил')
    message = models.TextField(verbose_name='Текст сообщения')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
