from django.contrib import admin
from .models import *


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death',
        'created_at',
        'updated_at',
    )

    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death')
    ]

    search_fields = ('last_name', 'first_name')

    inlines = [BookInline]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_at',
        'updated_at',
    )

    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'language',
        'created_at',
        'updated_at',
    )

    search_fields = ('language',)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author_name',
        'original_lang',
        'isbn',
        'display_genre',
        'created_at',
        'updated_at',
    )

    list_filter = ('created_at',)

    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book_title',
        'lang',
        'due_back',
        'status',
        'created_at',
        'updated_at',
    )

    list_filter = ('status', 'due_back', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Accessibility', {
            'fields': ('language',)
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
