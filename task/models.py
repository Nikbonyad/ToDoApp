from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=80, verbose_name="نام دسته‌بندی")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class StatusChoices(models.IntegerChoices):
    TODO = 0, 'برای انجام'
    DOING = 1, 'درحال انجام'
    COMPLETED = 2, 'انجام شده'


class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks',
                                 verbose_name="دسته‌بندی")
    title = models.CharField(max_length=80, verbose_name='عنوان')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    priority = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='اولویت')
    status = models.PositiveSmallIntegerField(choices=StatusChoices.choices, default=StatusChoices.TODO,
                                              verbose_name='وضعیت')
    deadline_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name="مهلت انجام")
    estimated_time = models.PositiveIntegerField(null=True, blank=True, help_text="زمان تخمینی بر حسب دقیقه",
                                                 validators=[MinValueValidator(1)], verbose_name="زمان تخمینی (دقیقه)")

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="آخرین تاریخ بروزرسانی")
    completed_at = jmodels.jDateTimeField(null=True, blank=True, verbose_name="تاریخ انجام")

    class Meta:
        db_table = 'tasks'
        verbose_name = 'وظیفه'
        verbose_name_plural = 'وظایف'

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.status == StatusChoices.COMPLETED.value and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != StatusChoices.COMPLETED.value:
            self.completed_at = None
        super().save(*args, **kwargs)
