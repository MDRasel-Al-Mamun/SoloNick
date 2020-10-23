from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'subject']
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message')

    class Meta:
        model = Contact


admin.site.register(Contact, ContactAdmin)
