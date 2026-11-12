from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Developer(models.Model):
    name = models.CharField(max_length=150, unique=True)
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1950), MaxValueValidator(2026)],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=100,unique=True)
    manufacturer = models.CharField(max_length=100,blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"

    def __str__(self):
        return self.name

class Game(models.Model):
    class Genre(models.TextChoices):
        ACTION = "action", "Action"
        RPG = "rpg", "RPG"
        STRATEGY = "strategy", "Strategy"
        SHOOTER = "shooter", "Shooter"
        SPORT = "sport", "Sport"
        RACING = "racing", "Racing"
        ADVENTURE = "adventure", "Adventure"
        UNKNOWN = "unknown", "Unknown"

    title = models.CharField(
        max_length=120
    )
    genre = models.CharField(
        max_length=50,
        choices=Genre.choices,
        default=Genre.UNKNOWN,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    released = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(2026)
        ]
    )
    developer = models.ForeignKey(
        Developer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games"
    )
    platforms = models.ManyToManyField(
        Platform,
        related_name="games",
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        indexes = [
            models.index(fields=["genre"], name="name_genre_idx"),
            models.index(fields=["released"], name="game_released_idx"),
            models.index(fields=["rating"], name="game_rating_idx")
        ]
    def __str__(self):
        return self.title
