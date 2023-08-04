from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'category',
        'location',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('author', 'category', 'location')
    list_display_links = ('title',)
    empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('slug',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )

    list_editable = (
        'is_published',
    )

    search_fields = ('name',)
    list_display_links = ('name',)
