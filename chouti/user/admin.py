from django.contrib import admin
from . import models
# Register your models here.
class UserInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.UserInfo, UserInfoAdmin)

class SendMsgAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.SendMsg, SendMsgAdmin)