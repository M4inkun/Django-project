from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator


class PublisherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_publisher=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг',
                            validators=[
                                MinLengthValidator(5, message='Минимум 5 символов'),
                                MaxLengthValidator(100, message='Максимум 100 символов')
                            ])
    content = models.TextField(blank=True, verbose_name='Содержимое')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_publisher = models.BooleanField(choices=tuple(map(lambda status: (bool(status[0]), status[1]), Status.choices)), default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tag = models.ManyToManyField('ModelTags', blank=True, related_name='tags', verbose_name='Тэги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman', verbose_name='Муж')

    objects = models.Manager()
    published = PublisherManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известные женщины мира'
        verbose_name_plural = 'Известные женщины мира'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class ModelTags(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name

