from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    #kodom fild haro neshon bede
    list_display = ('user', 'slug', 'updated')
    #search bara kodom fild bash.
    #inja to in tuple mitoni chanta fild bezari
    search_fields = ('slug',)
    list_filter = ('updated',)
    #kadr filter samt rast
    prepopulated_fields = {'slug':('body',)}
    #slug ro miyad bar hasb body por mikone(otomatic)
    raw_id_fields = ('user',)
    #fild user ro ba id por mikone
admin.site.register(Post,PostAdmin)

# Register your models here.
