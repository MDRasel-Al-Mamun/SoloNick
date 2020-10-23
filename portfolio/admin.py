from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'date']
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class PortfolioDetailsInline(admin.TabularInline):
    model = Details
    extra = 3


class PortfolioImageInline(admin.TabularInline):
    model = Images
    extra = 2


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'client', 'status', 'thumbnail_tag']
    list_filter = ['category']
    readonly_fields = ['thumbnail_tag']
    inlines = [PortfolioDetailsInline, PortfolioImageInline]
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10

    class Meta:
        model = Portfolio


admin.site.register(Portfolio, PortfolioAdmin)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image_tag']
    search_fields = ['__str__']

    class Meta:
        model = Images


admin.site.register(Images, ImagesAdmin)


class DetailsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'detail']

    class Meta:
        model = Details


admin.site.register(Details, DetailsAdmin)
