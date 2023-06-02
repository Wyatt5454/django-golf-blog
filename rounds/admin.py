from django.contrib import admin

from .models import Player, Round, HoleScore

# Register your models here.
class HoleScoreInline(admin.TabularInline):
    model = HoleScore
    extra = 18
    max_num = 18

class RoundAdmin(admin.ModelAdmin):
    inlines = [HoleScoreInline]
    list_display = ["play_date", "tee_played", "total_score"]
    list_filter = ["play_date"]
    search_fields = ["tee_played"]

class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Round, RoundAdmin)
admin.site.register(Player, PlayerAdmin)
