from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from datetime import date
from .models import(
    Departments,
    Equipment,
    BaseUserProfile,
    User,
    EmploymentInformation,
    Miscellaneous,
    EquipmentAllocation,
)


class UsersManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)

    def test_position_default(self):
        # Test default position value
        user = self.User.objects.create_user(email="test@user.com", password="foo")
        self.assertEqual(user.position, 'man')


# Define a test class for Departments model
class DepartmentsModelTest(TestCase):
    # Define a setup method to initialize test data
    def setUp(self):
        # Create a department object for testing
        self.department = Departments.objects.create(name='Test Department')

    # Define test methods to test model functionality
    def test_department_creation(self):
        # Test if the department object was created successfully
        self.assertTrue(isinstance(self.department, Departments))
        
    def test_department_name_display(self):
        # Test if the department name is properly displayed
        self.assertEqual(str(self.department), 'Test Department')

    def test_department_representation(self):
        # Test if the department can be represented as a string
        self.assertEqual(repr(self.department), '<Departments: Test Department>')

# Define a test class for Equipment model
class EquipmentModelTest(TestCase):
    # Define a setup method to initialize test data
    def setUp(self):
        # Create an equipment object for testing
        self.equipment = Equipment.objects.create(name='Test Equipment', total_number=10)

    # Define test methods to test model functionality
    def test_equipment_creation(self):
        # Test if the equipment object was created successfully
        self.assertTrue(isinstance(self.equipment, Equipment))
        
    def test_equipment_name_display(self):
        # Test if the equipment name is properly displayed
        self.assertEqual(str(self.equipment), 'Test Equipment')

    def test_equipment_total_number_display(self):
        # Test if the total number of equipment is properly displayed
        self.assertEqual(self.equipment.total_number, 10)

    def test_equipment_representation(self):
        # Test if the equipment can be represented as a string
        self.assertEqual(repr(self.equipment), '<Equipment: Test Equipment>')

class BaseUserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.base_user_profile = BaseUserProfile.objects.create(
            user=self.user,
            surname='Doe',
            given_name='John',
            gender='male',
            contact='0123456789',
            location='Test Location',
            next_of_kin='Jane Doe',
            emergency_contact='9876543210',
            date_of_birth=date(1990, 1, 1),
            place_of_birth='Test Place',
            age=30,
            nin='ABC123456789',
        )

    def test_base_user_profile_creation(self):
        self.assertTrue(isinstance(self.base_user_profile, BaseUserProfile))
        self.assertEqual(self.base_user_profile.__str__(), 'Doe John')
        self.assertEqual(self.base_user_profile.surname, 'Doe')
        self.assertEqual(self.base_user_profile.given_name, 'John')
        self.assertEqual(self.base_user_profile.gender, 'male')
        self.assertEqual(self.base_user_profile.contact, '0123456789')
        self.assertEqual(self.base_user_profile.location, 'Test Location')
        self.assertEqual(self.base_user_profile.next_of_kin, 'Jane Doe')
        self.assertEqual(self.base_user_profile.emergency_contact, '9876543210')
        self.assertEqual(self.base_user_profile.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.base_user_profile.place_of_birth, 'Test Place')
        self.assertEqual(self.base_user_profile.age, 30)
        self.assertEqual(self.base_user_profile.nin, 'ABC123456789')

# Define a test class for EmploymentInformation model
class EmploymentInformationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.department = Departments.objects.create(name='Test Department')
        self.employment_info = EmploymentInformation.objects.create(
            user=self.user,
            employment_status='ft',
            department=self.department,
            employment_start_date=date(2023, 1, 1),
            head_of_department=self.user,
        )

    def test_employment_information_creation(self):
        self.assertTrue(isinstance(self.employment_info, EmploymentInformation))
        self.assertEqual(self.employment_info.__str__(), 'ft employment in Test Department department')
        self.assertEqual(self.employment_info.user, self.user)
        self.assertEqual(self.employment_info.employment_status, 'ft')
        self.assertEqual(self.employment_info.department, self.department)
        self.assertEqual(self.employment_info.employment_start_date, date(2023, 1, 1))
        self.assertEqual(self.employment_info.head_of_department, self.user)

# Define a test class for Miscellaneous model
class MiscellaneousModelTest(TestCase):
    # Define a setup method to initialize test data
    def setUp(self):
        # Create a user object for testing
        self.user = User.objects.create(email='test@example.com')
        # Create a miscellaneous object for testing
        self.miscellaneous = Miscellaneous.objects.create(
            user=self.user,
            salary=50000.00,
            payment='Bank Account',
            userid='01',
            ackno=True
        )

    # Define test methods to test model functionality
    def test_miscellaneous_creation(self):
        # Test if the miscellaneous object was created successfully
        self.assertTrue(isinstance(self.miscellaneous, Miscellaneous))
        
    def test_miscellaneous_representation(self):
        # Test if the miscellaneous can be represented as a string
        expected_representation = f"Miscellaneous info for {self.user.email}"
        self.assertEqual(str(self.miscellaneous), expected_representation)

# Define a test class for EquipmentAllocation model
class EquipmentAllocationModelTest(TestCase):
    # Define a setup method to initialize test data
    def setUp(self):
        # Create a user object for testing
        self.user = User.objects.create(email='test@example.com')
        # Create an equipment object for testing
        self.equipment = Equipment.objects.create(name='Test Equipment', total_number=10)
        # Create an equipment allocation object for testing
        self.equipment_allocation = EquipmentAllocation.objects.create(
            user=self.user,
            equipment=self.equipment,
            quantity_allocated=5
        )

    # Define test methods to test model functionality
    def test_equipment_allocation_creation(self):
        # Test if the equipment allocation object was created successfully
        self.assertTrue(isinstance(self.equipment_allocation, EquipmentAllocation))
        
    def test_equipment_allocation_representation(self):
        # Test if the equipment allocation can be represented as a string
        expected_representation = "5 Test Equipment allocated to test@example.com"
        self.assertEqual(str(self.equipment_allocation), expected_representation)


# tests for model relationship
class ModelRelationshipTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.department = Departments.objects.create(name='Test Department')

    def test_user_profile_relationship(self):
        profile = BaseUserProfile.objects.create(
            user=self.user,
            surname='Test',
            given_name='User',
            gender='male',
            contact='0123456789',
            location='Test Location',
            next_of_kin='Test Next of Kin',
            emergency_contact='987654321',
            date_of_birth='1990-01-01',
            place_of_birth='Test Place of Birth',
            age=30
        )
        self.assertEqual(self.user.profile, profile)

    def test_user_employment_info_relationship(self):
        employment_info = EmploymentInformation.objects.create(
            user=self.user,
            employment_status='ft',
            department=self.department,  # Pass the Departments instance here
            employment_start_date=timezone.now().date(),  # You can use timezone.now() for the current date
        )
        self.assertEqual(self.user.employment_info, employment_info)
    def test_user_miscellaneous_relationship(self):
        misc = Miscellaneous.objects.create(
            user=self.user,
            salary=50000,
            payment='Bank Account',
            userid='01',
            ackno=True
        )
        self.assertEqual(self.user.miscella, misc)

    def test_user_equipment_allocation_relationship(self):
        equipment = Equipment.objects.create(name='Uniform', total_number=100)
        allocation = EquipmentAllocation.objects.create(
            user=self.user,
            equipment=equipment,
            quantity_allocated=2
        )
        self.assertIn(allocation, self.user.equipment_allocations.all())