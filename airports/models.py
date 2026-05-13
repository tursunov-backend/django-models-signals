from django.db import models
from django.utils.text import slugify


class Airport(models.Model):
    class AirportType(models.TextChoices):
        INTERNATIONAL = "international", "International"
        DOMESTIC = "domestic", "Domestic"
        PRIVATE = "private", "Private"
        MILITARY = "military", "Military"
        CARGO = "cargo", "Cargo"

    # Core Information
    airport_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="IATA or ICAO airport code",
    )
    icao_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        db_index=True,
    )

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True)

    # Location
    city = models.CharField(max_length=255, db_index=True)
    city_code = models.CharField(max_length=10, db_index=True)

    state = models.CharField(max_length=255, blank=True, null=True)
    state_code = models.CharField(max_length=10, blank=True, null=True)

    country = models.CharField(max_length=255, db_index=True)
    country_code = models.CharField(max_length=10, db_index=True)

    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    timezone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Example: Asia/Tashkent",
    )

    # Airport Details
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.INTERNATIONAL,
    )

    terminals = models.PositiveIntegerField(default=1)
    runways = models.PositiveIntegerField(default=1)

    elevation_ft = models.IntegerField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Operational
    is_active = models.BooleanField(default=True)
    is_24_hours = models.BooleanField(default=False)
    supports_cargo = models.BooleanField(default=False)
    supports_international_flights = models.BooleanField(default=True)

    # SEO / Metadata
    description = models.TextField(blank=True, null=True)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "airports"
        ordering = ["country", "city", "name"]
        indexes = [
            models.Index(fields=["airport_code"]),
            models.Index(fields=["icao_code"]),
            models.Index(fields=["city"]),
            models.Index(fields=["city_code"]),
            models.Index(fields=["country"]),
            models.Index(fields=["country_code"]),
            models.Index(fields=["name"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.airport_code}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.airport_code})"
    
# /api/airports/?search=Tashkent - search by name, city, country, airport code, etc.
