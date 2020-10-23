from django.contrib import admin
from .models import *


class MyProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'avatar_tag', 'designation', 'status']

    class Meta:
        model = MyProfile


admin.site.register(MyProfile, MyProfileAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'create_at']

    class Meta:
        model = Service


admin.site.register(Service, ServiceAdmin)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'institute', 'year', 'status']

    class Meta:
        model = Resume


admin.site.register(Resume, ResumeAdmin)


class PresentationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image_tag', 'date']

    class Meta:
        model = Presentation


admin.site.register(Presentation, PresentationAdmin)
