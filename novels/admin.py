from django.contrib import admin
from .models import   Authors, Library, LibraryModel, Novel, NovelChapter,Review, Comment,Reply_Comment,Reply_Review, Status
# Register your models here.
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Reply_Review)
admin.site.register(Reply_Comment)
admin.site.register(Status)
admin.site.register(LibraryModel)


class NovelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title']
    list_display = ('id', 'title')

admin.site.register(Novel, NovelAdmin)  

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('author',), }
admin.site.register(Authors, AuthorAdmin)    


class NovelChaptersAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title']
    
admin.site.register(NovelChapter,NovelChaptersAdmin)

@admin.register(Library)
class FavoritesProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'products_count')
    list_display_links = ('id', 'user')
    list_per_page = 25
    