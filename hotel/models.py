from django.db import models

# Room category class
class Category(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    capacity = models.PositiveIntegerField()
    count = models.PositiveBigIntegerField(
        help_text='number of rooms in this category.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Room Category"
        verbose_name_plural = "Room Categories"
    
    def __str__(self):
        return self.name
# Rooms model
class Room(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=30,
    )
    room_number = models.CharField(
        null=True,
        blank=True,
        max_length=3,
    )
    floor_number = models.CharField(
        null=True,
        blank=True,
        max_length=2,
        help_text='Location of the room on the building counting from the bottom level.'
    )
    description = models.TextField()
    capacity = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('out_of_service', 'Out of Service'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Room No. {self.room_number}"
