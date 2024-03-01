from django.test import TestCase
import unittest
from django.utils import timezone
from .models import Booking, Room, Guest, Reservation, PaymentInformation, Category
from choices.models import RoomStatus, BookingStatus, BookingSource

class CategoryTestCase(TestCase):
    def setUp(self):
        # Create a RoomStatus instance
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            price=100.00,
            capacity=2,
        )

    def test_update_room_count(self):
        """
        Test if update_room_count method updates the room_count correctly
        """
        status = RoomStatus.objects.create(room_status='Default Status')
        try:
            # Create some rooms for the category
            for _ in range(3):
                Room.objects.create(category=self.category, status=status)  # Provide status instance
        except Exception as e:
            # Handle integrity error caused by NOT NULL constraint on status_id
            self.fail("Failed to create rooms: {}".format(e))

        # Call the method to update room count
        self.category.update_room_count()

        # Check if room count is updated correctly
        self.assertEqual(self.category.room_count, 3)
class RoomTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            price=100.00,
            capacity=2,
        )
        self.status = RoomStatus.objects.create(room_status='Available')
        self.room = Room.objects.create(
            category=self.category,
            name='Test Room',
            room_number='101',
            floor_number='1',
            description='Test Room Description',
            capacity=2,
            status=self.status,
            standard_price=150.00,
            discount=10,
        )

    def test_room_creation(self):
        """
        Test if a room is created correctly
        """
        self.assertEqual(self.room.name, 'Test Room')
        self.assertEqual(self.room.room_number, '101')
        self.assertEqual(self.room.floor_number, '1')
        self.assertEqual(self.room.description, 'Test Room Description')
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.status, self.status)
        self.assertEqual(self.room.standard_price, 150.00)
        self.assertEqual(self.room.promotional_price, 135.00)  # Promotional price after applying discount

    def test_room_deletion(self):
        """
        Test if a room deletion updates the room count for the category
        """
        initial_room_count = self.category.room_count
        self.room.delete()
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.room_count, initial_room_count - 1)

    def test_promotional_price_calculation(self):
        """
        Test if promotional price is calculated correctly based on standard price and discount
        """
        self.assertEqual(self.room.promotional_price, 135.00)

    def test_room_count_update_on_creation(self):
        """
        Test if room count for the category updates when a room is created
        """
        initial_room_count = self.category.room_count
        Room.objects.create(
            category=self.category,
            name='Another Test Room',
            room_number='102',
            floor_number='1',
            description='Another Test Room Description',
            capacity=2,
            status=self.status,
            standard_price=200.00,
            discount=0,
        )
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.room_count, initial_room_count + 1)

if __name__ == '__main__':
    unittest.main()