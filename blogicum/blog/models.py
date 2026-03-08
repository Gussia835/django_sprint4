from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class PublishedManager(models.Manager):
    """Менеджер для получения только опубликованных постов."""

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'location', 'category'
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                'category',
                'author',
                'location',
            )
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
            .order_by('-pub_date')
        )

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                                    'чтобы скрыть публикацию.')

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=256,
                            verbose_name='Название места')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Category(BaseModel):
    title = models.CharField(max_length=256,
                             verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, дефис '
                            'и подчёркивание.')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Post(BaseModel):
    title = models.CharField(max_length=256,
                             verbose_name='Заголовок')
    
    text = models.TextField(verbose_name='Текст')

    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — можно делать '
                                    'отложенные публикации.')
    
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='posts_image',
                              blank=True)
    
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации',
                               related_name='posts')
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Местоположение',
                                 related_name='posts')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',
                                 related_name='posts')

    objects = models.Manager()
    post_list = PostManager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']


class Comment(BaseModel):
    author = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name='Автор',
                                  related_name='author_comments')

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='Пост',
                             related_name='comments')

    content = models.TextField(verbose_name='Текст комментария')

    created_at = models.DateTimeField(verbose_name='Время создания',
                                      auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.content
