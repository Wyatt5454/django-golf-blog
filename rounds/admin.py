from django.contrib import admin

from .models import Player, Round, HoleScore, HoleDisplay, Course, Tee

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

class HoleDisplayInline(admin.TabularInline):
    model = HoleDisplay
    extra = 18
    max_num = 18

class CourseAdmin(admin.ModelAdmin):
    inlines = [HoleDisplayInline]
    list_display = ["name", "description"]
    list_filter = ["name"]
    search_fields = ["name"]

class TeeAdmin(admin.ModelAdmin):
    list_display = ["course", "name", "yardage", "slope"]
    list_filter = ["course"]
    search_fields = ["course", "name", "yardage", "slope"]

admin.site.register(Round, RoundAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tee, TeeAdmin)
