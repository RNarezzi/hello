import unittest
from unittest.mock import MagicMock
from src.user_service import UserService, Database

class TestUserService(unittest.TestCase):
    def test_get_user_name(self):
        # Create a mock for the Database class
        mock_database = MagicMock(spec=Database)

        # Define the behavior of the mock's get_user method
        mock_database.get_user.return_value = {'id': 1, 'name': 'Alice'}

        # Instantiate the UserService with the mock database
        user_service = UserService(mock_database)

        # Call the method we want to test
        user_name = user_service.get_user_name(1)

        # Assertions
        self.assertEqual(user_name, 'Alice')
        mock_database.get_user.assert_called_once_with(1)

    def test_get_user_name_not_found(self):
        # Create a mock for the Database class
        mock_database = MagicMock(spec=Database)

        # Define the behavior for when user is not found
        mock_database.get_user.return_value = None

        # Instantiate the UserService with the mock database
        user_service = UserService(mock_database)

        # Call the method we want to test
        user_name = user_service.get_user_name(99)

        # Assertions
        self.assertIsNone(user_name)
        mock_database.get_user.assert_called_once_with(99)

if __name__ == '__main__':
    unittest.main()
