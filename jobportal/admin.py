from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserModelAdmin

# Register your models here.
# class RegisterAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name','email','mobile']
#     readonly_fields = ['register_id']
# admin.site.register(Register, RegisterAdmin)

class UserModelAdmin(BaseUserModelAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'name', 'mobile', 'is_admin')
    readonly_fields = ['register_id']
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobile', 'register_id')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)