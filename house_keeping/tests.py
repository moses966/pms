from django.test import TestCase
from django.utils import timezone
from .models import HousekeepingTask, MaintenanceRequest, CleanRoom
from management.models import BaseUserProfile
from django.contrib.auth import get_user_model
from hotel.models import Room

class HousekeepingTaskCreationTest(TestCase):
    def setUp(self):
        # Create a Room instance for association
        self.room = Room.objects.create(room_number='101', floor_number=1, status='available')

    def test_create_housekeeping_task(self):
        # Create a new HousekeepingTask instance
        task = HousekeepingTask.objects.create(room_number=self.room)
        
        # Verify room association
        self.assertEqual(task.room_number, self.room)

        # Check default status
        self.assertEqual(task.task_status, 'pending')

        # Confirm creation timestamp
        current_time = timezone.now()
        self.assertLessEqual(task.created_at, current_time)
        self.assertGreaterEqual(task.created_at, current_time - timezone.timedelta(seconds=1))

class MaintenanceRequestCreationTest(TestCase):
    def setUp(self):
        # Create a Room instance for association
        self.room = Room.objects.create(room_number='102', floor_number=1, status='available')

    def test_create_maintenance_request(self):
        # Create a new HousekeepingTask instance
        task = HousekeepingTask.objects.create(room_number=self.room)

        # Create a new User instance
        User = get_user_model()
        user = User.objects.create_user(email='user@example.com', password='password')

        # Create a new BaseUserProfile instance and associate it with the user
        profile = BaseUserProfile.objects.create(user=user, surname='John', given_name='Doe', gender='male',
                 contact='1234567890', location='Some Location', next_of_kin='Jane Doe',
                 emergency_contact='0987654321', date_of_birth='1990-01-01', place_of_birth='Some Place',
                 age=30, nin='123456789012345678901234',
        )

        # Create a new MaintenanceRequest instance and link it to the HousekeepingTask
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Verify association with HousekeepingTask
        self.assertEqual(maintenance_request.housekeeping_task, task)

        # Assign user's profile to the MaintenanceRequest
        maintenance_request.assigned_to.add(profile)

        # Check assigned users
        self.assertIn(profile, maintenance_request.assigned_to.all())

        # Confirm creation timestamp
        current_time = timezone.now()
        self.assertLessEqual(maintenance_request.created_at, current_time)
        self.assertGreaterEqual(maintenance_request.created_at, current_time - timezone.timedelta(seconds=1))

class MaintenanceRequestAssignUsersTest(TestCase):
    def setUp(self):
        self._counter = 1  # Initialize the counter
        # Create user profiles without email
        self.user1 = self.create_user_profile(surname='Doe', given_name='John', gender='male',
                                              contact='1234567890', location='Location 1', next_of_kin='Jane Doe',
                                              emergency_contact='0987654321', date_of_birth='1990-01-01', place_of_birth='Place 1',
                                              age=30, nin='123456789012345678901234')

        self.user2 = self.create_user_profile(surname='Smith', given_name='Alice', gender='female',
                                              contact='9876543210', location='Location 2', next_of_kin='John Smith',
                                              emergency_contact='0123456789', date_of_birth='1995-02-15', place_of_birth='Place 2',
                                              age=25, nin='987654321098765432109876')

    def create_user_profile(self, **kwargs):
        User = get_user_model()
        email = f"{self.__class__.__name__.lower()}_{self._counter}@example.com"
        self._counter += 1  # Increment the counter
        user = User.objects.create_user(email=email, password='password')
        return BaseUserProfile.objects.create(user=user, **kwargs)

    def test_assign_users_to_maintenance_request(self):
        # Create a new HousekeepingTask instance
        room = Room.objects.create(room_number='103', floor_number=1, status='available')
        task = HousekeepingTask.objects.create(room_number=room)

        # Create a new MaintenanceRequest instance
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Assign user profiles to the MaintenanceRequest
        maintenance_request.assigned_to.add(self.user1, self.user2)

        # Check assigned users
        assigned_users = maintenance_request.assigned_to.all()
        self.assertIn(self.user1, assigned_users)
        self.assertIn(self.user2, assigned_users)

class MaintenanceRequestDeletionTest(TestCase):
    def setUp(self):
        # Create a Room instance for association
        self.room = Room.objects.create(room_number='103', floor_number=1, status='available')

    def test_delete_maintenance_request(self):
        # Create a new HousekeepingTask instance
        task = HousekeepingTask.objects.create(room_number=self.room)

        # Create a new MaintenanceRequest instance and link it to the HousekeepingTask
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Delete the MaintenanceRequest instance
        maintenance_request.delete()

        # Verify that the instance is deleted
        with self.assertRaises(MaintenanceRequest.DoesNotExist):
            MaintenanceRequest.objects.get(pk=maintenance_request.pk)

    def test_delete_maintenance_request_with_clean_room(self):
        # Create a new HousekeepingTask instance
        task = HousekeepingTask.objects.create(room_number=self.room)

        # Create a new MaintenanceRequest instance and link it to the HousekeepingTask
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Create a CleanRoom instance associated with the HousekeepingTask's room
        # This simulates an existing CleanRoom instance
        clean_room = task.room_number.clean_room.create()

        # Delete the MaintenanceRequest instance
        maintenance_request.delete()

        # Ensure that associated CleanRoom instance is deleted
        with self.assertRaises(CleanRoom.DoesNotExist):
            CleanRoom.objects.get(pk=clean_room.pk)