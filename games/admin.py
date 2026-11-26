from django.contrib import admin
from django.db.models import Count

from .models import Developer, Game, Platform


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "genre",
        "rating",
        "released",
        "developer",
        "created_at",
    )
    list_display_links = ("title",)
    list_filter = ("genre", "released", "developer", "platforms")
    search_fields = ("title", "developer__name", "platforms__name")
    ordering = ("title",)
    filter_horizontal = ("platforms",)
    list_select_related = ("developer",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    fieldsets = (
        ("Основная информация", {"fields": ("title", "genre", "rating", "released")}),
        ("Связи", {"fields": ("developer", "platforms")}),
        ("Служебная информация", {"fields": ("created_at",)}),
    )


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "founded_year", "game_count")
    list_filter = ("country",)
    search_fields = ("name", "country")
    ordering = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(games_total=Count("games"))

    @admin.display(description="Игр")
    def game_count(self, developer):
        return developer.games_total


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "game_count")
    search_fields = ("name", "manufacturer")
    ordering = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(games_total=Count("games"))

    @admin.display(description="Игр")
    def game_count(self, platform):
        return platform.games_total


admin.site.site_header = "Каталог видеоигр"
admin.site.site_title = "Администрирование каталога"
admin.site.index_title = "Управление каталогом"