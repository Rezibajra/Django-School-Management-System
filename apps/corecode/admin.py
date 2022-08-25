from django.contrib import admin
# from django.utils.timezone import localtime
from .models import Mark, Subject, AcademicTerm, MarkAuditLog

admin.site.register(Mark)
admin.site.register(Subject)
admin.site.register(AcademicTerm)

# class YourModelAdmin(admin.ModelAdmin):
#     updated_at = localtime(otp_obj.updated_at)
#     readonly_fields = ('created_at', 'updated_at', )
admin.site.register(MarkAuditLog)
