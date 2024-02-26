from django.db import models

class Positions(models.Model):
    position = models.CharField(max_length=20)

    def __str__(self):
        return self.position
    def save(self, *args, **kwargs):
        # Convert position to lowercase before saving
        self.position = self.position.lower()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Individual Position'
        verbose_name_plural = 'Individual Positions'


class RoomStatus(models.Model):
    room_status = models.CharField(max_length=20)

    def __str__(self):
        return self.room_status
    def save(self, *args, **kwargs):
        # Convert room_status to lowercase before saving
        self.room_status = self.room_status.lower()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Room Status'
        verbose_name_plural = 'Room Status'

class BookingSource(models.Model):
    booking_source = models.CharField(max_length=20)

    def __str__(self):
        return self.booking_source
    
    def save(self, *args, **kwargs):
        self.booking_source = self.booking_source.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Booking Channel'
        verbose_name_plural = 'Booking Channels'

class BookingStatus(models.Model):
    booking_status = models.CharField(max_length=20)

    def __str__(self):
        return self.booking_status
    
    def save(self, *args, **kwargs):
        self.booking_status = self.booking_status.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Booking Status'
        verbose_name_plural = 'Booking Status'

class GenderChoices(models.Model):
    gender_choices = models.CharField(max_length=20)

    def __str__(self):
        return self.gender_choices
    
    def save(self, *args, **kwargs):
        self.gender_choices = self.gender_choices.lower()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Gender Choice'
        verbose_name_plural = 'Gender Choices'


class ReservationStatus(models.Model):
    reservation_status = models.CharField(max_length=20)

    def __str__(self):
        return self.reservation_status
    
    def save(self, *args, **kwargs):
        self.reservation_status = self.reservation_status.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Reservation Status'
        verbose_name_plural = 'Reservation Status'


class PaymentStatus(models.Model):
    payment_status = models.CharField(max_length=20)

    def __str__(self):
        return self.payment_status
    
    def save(self, *args, **kwargs):
        self.payment_status = self.payment_status.lower()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Payment Status'
        verbose_name_plural = 'Payment Status'


class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=20)

    def __str__(self):
        return self.payment_method
    
    def save(self, *args, **kwargs):
        self.payment_method = self.payment_method.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'


class EmploymentStatus(models.Model):
    employment_status = models.CharField(max_length=20)

    def __str__(self):
        return self.employment_status
    
    def save(self, *args, **kwargs):
        self.employment_status = self.employment_status.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Employment Status'
        verbose_name_plural = 'Employment Status'

class EmployPaymentMethod(models.Model):
    payment_method = models.CharField(max_length=20)

    def __str__(self):
        return self.employment_status
    
    def save(self, *args, **kwargs):
        self.payment_method = self.payment_method.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Salary Payment Channel'
        verbose_name_plural = 'Salary Payment Channels'

class MenuAndDrinksChoice(models.Model):
    food_or_drink = models.CharField(max_length=20)

    def __str__(self):
        return self.food_or_drink
    
    def save(self, *args, **kwargs):
        self.food_or_drink = self.food_or_drink.lower()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Food or Drink Choice'
        verbose_name_plural = 'Food or Drinks Choices'


