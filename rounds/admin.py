from django.contrib import admin

from .models import Player, Round, Hole

# Register your models here.
class HoleInline(admin.TabularInline):
    model = Hole
    extra = 18
    max_num = 18

class RoundAdmin(admin.ModelAdmin):
    inlines = [HoleInline]
    list_display = ["play_date", "course", "total_score"]
    list_filter = ["play_date", "course"]
    search_fields = ["course"]

class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Round, RoundAdmin)
admin.site.register(Player, PlayerAdmin)
