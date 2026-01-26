from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from .models import Task, StatusChoices


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'deadline_time', 'is_delayed')
    list_filter = ('status', ('created_at', JDateFieldListFilter), 'category')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'title', 'category', 'description')
        }),
        ('وضعیت و زمان‌بندی', {
            'fields': (('status', 'priority'), ('estimated_time', 'deadline_time'))
        }),
        ('تاریخچه سیستم', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )

    def is_delayed(self, obj):
        from django.utils import timezone
        if obj.deadline_time and obj.status != StatusChoices.COMPLETED.value:
            return timezone.now() > obj.deadline_time
        return False

    is_delayed.boolean = True
    is_delayed.short_description = 'تأخیر دارد؟'
