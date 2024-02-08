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
                    age=30, nin='123456789012345678901234',
        )

        self.user2 = self.create_user_profile(surname='Smith', given_name='Alice', gender='female',
                    contact='9876543210', location='Location 2', next_of_kin='John Smith',
                    emergency_contact='0123456789', date_of_birth='1995-02-15', place_of_birth='Place 2',
                    age=25, nin='987654321098765432109876',
        )

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

    def test_delete_maintenance_request_with_clean_room(self):
        # Create a new HousekeepingTask instance
        task = HousekeepingTask.objects.create(room_number=self.room)

        # Create a CleanRoom instance associated with the HousekeepingTask's room
        clean_room = CleanRoom.objects.create(room=task.room_number)

        # Create a new MaintenanceRequest instance and link it to the HousekeepingTask
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Delete the MaintenanceRequest instance
        maintenance_request.delete()

        # Ensure that associated CleanRoom instance is deleted
        with self.assertRaises(CleanRoom.DoesNotExist):
            CleanRoom.objects.get(pk=clean_room.pk)

class HousekeepingTaskMethodTest(TestCase):
    def setUp(self):
        # Create a Room instance for association
        self.room = Room.objects.create(room_number='104', floor_number=1, status='available')

    def test_handle_clean_room_pending_task(self):
        # Create a new HousekeepingTask instance with status 'pending'
        task = HousekeepingTask.objects.create(room_number=self.room, task_status='pending')

        # Call the handle_clean_room method
        task.handle_clean_room()

        # Verify CleanRoom is not created for pending task
        clean_room = CleanRoom.objects.filter(room=self.room).first()
        self.assertIsNone(clean_room)

    def test_handle_clean_room_non_pending_task(self):
        # Create a new HousekeepingTask instance with status other than 'pending'
        task = HousekeepingTask.objects.create(room_number=self.room, task_status='in_progress')

        # Create a CleanRoom instance for the associated room
        clean_room = CleanRoom.objects.create(room=self.room)

        # Call the handle_clean_room method
        task.handle_clean_room()

        # Verify CleanRoom is not deleted for non-pending task
        clean_room_exists = CleanRoom.objects.filter(room=self.room).exists()
        self.assertTrue(clean_room_exists)

class MaintenanceRequestSaveMethodTest(TestCase):
    def setUp(self):
        # Create a Room instance for association
        self.room = Room.objects.create(room_number='105', floor_number=1, status='available')

    def test_save_method_resolved_true(self):
        # Create a MaintenanceRequest instance with resolved set to True
        task = HousekeepingTask.objects.create(room_number=self.room)
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task, resolved=True)

        # Call the save method
        maintenance_request.save()

        # Verify associated HousekeepingTask's task_status is updated to 'completed'
        task.refresh_from_db()
        self.assertEqual(task.task_status, 'completed')

        # Verify CleanRoom instance is created for associated room
        clean_room = CleanRoom.objects.filter(room=self.room).first()
        self.assertIsNotNone(clean_room)

    def test_save_method_in_progress_true(self):
        # Create a MaintenanceRequest instance with in_progress set to True
        task = HousekeepingTask.objects.create(room_number=self.room)
        clean_room = CleanRoom.objects.create(room=self.room)  # Create CleanRoom for association
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task, in_progress=True)

        # Call the save method
        maintenance_request.save()

        # Verify associated HousekeepingTask's task_status is updated to 'in_progress'
        task.refresh_from_db()
        self.assertEqual(task.task_status, 'in_progress')

        # Verify CleanRoom instance is deleted
        clean_room_exists = CleanRoom.objects.filter(room=self.room).exists()
        self.assertFalse(clean_room_exists)

class MaintenanceRequestDeleteMethodTest(TestCase):
    def setUp(self):
        # Create a Room instance for association
        self.room = Room.objects.create(room_number='106', floor_number=1, status='available')

    def test_delete_method_with_clean_room(self):
        # Create a MaintenanceRequest instance
        task = HousekeepingTask.objects.create(room_number=self.room)
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Create a CleanRoom instance for the associated room
        clean_room = CleanRoom.objects.create(room=self.room)

        # Delete the MaintenanceRequest instance
        maintenance_request.delete()

        # Verify that the associated CleanRoom instance is deleted
        clean_room_exists = CleanRoom.objects.filter(room=self.room).exists()
        self.assertFalse(clean_room_exists)

    def test_delete_method_without_clean_room(self):
        # Create a MaintenanceRequest instance
        task = HousekeepingTask.objects.create(room_number=self.room)
        maintenance_request = MaintenanceRequest.objects.create(housekeeping_task=task)

        # Delete the MaintenanceRequest instance
        maintenance_request.delete()

        # Verify that no error is raised if there's no associated CleanRoom instance
        clean_room_exists = CleanRoom.objects.filter(room=self.room).exists()
        self.assertFalse(clean_room_exists)