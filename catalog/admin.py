from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

#admin.site.register(Book)  
# admin.site.register(Author) # простая регистрация отображения


admin.site.register(Genre)
#admin.site.register(BookInstance)

# Register the Admin classes for Book using the decorator
class BooksInstanceInline(admin.TabularInline): #https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.TabularInline
    model = BookInstance      # ип TabularInline (горизонтальное расположение) или StackedInline

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre') # замена или дополненеие str метода
    inlines = [BooksInstanceInline] #     https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines
                    #  получить и информацию о книге, ю о конкретных копиях, зайдя на страницу детализации.

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status', 'due_back', 'id' )  # добавление фильтра
    #(self.book.title, self.status, self.due_back, self.id)
    fieldsets = (   # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    (None, {
        'fields': ('book','imprint', 'id')
    }),
    ('Availability', {
        'fields': ('status', 'due_back')
    }),
)   
    
class BooksInline(admin.TabularInline): #https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.TabularInline
    model = Book  
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BooksInline] #     https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines
 
    #ModelAdmin.list_display
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
        # манипулирование формой верху , в низ (с лева ,направо )
