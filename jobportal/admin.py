from django.contrib import admin
from .models import Register

# Register your models here.
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','email','mobile']
    readonly_fields = ['register_id']
admin.site.register(Register, RegisterAdmin)