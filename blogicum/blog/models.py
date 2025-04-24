from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PublishedBaseModel(models.Model):
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
        null=False,
        blank=False,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        verbose_name="Добавлено", auto_now_add=True, null=False, blank=False
    )

    class Meta:
        abstract = True


class PostBaseModel(PublishedBaseModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Автор публикации",
        related_name="%(class)ss",
    )
    text = models.TextField("Текст", null=False, blank=False)

    class Meta:
        abstract = True


class Post(PostBaseModel):
    title = models.CharField(
        verbose_name="Заголовок", max_length=256, null=False, blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        null=False,
        blank=False,
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField(
        verbose_name="Фото", upload_to="post_images", blank=True
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.title}, {self.author}"


class Category(PublishedBaseModel):
    title = models.CharField(
        verbose_name="Заголовок", max_length=256, null=False, blank=False
    )
    description = models.TextField(
        verbose_name="Описание", null=False, blank=False
    )
    slug = models.SlugField(
        verbose_name="Идентификатор",
        unique=True,
        null=False,
        blank=False,
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(PublishedBaseModel):
    name = models.CharField(
        verbose_name="Название места", max_length=256, null=False, blank=False
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Comment(PostBaseModel):
    post = models.ForeignKey(
        Post,
        verbose_name="Пост",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="comments",
    )
    is_published = None

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return self.text[:50]
