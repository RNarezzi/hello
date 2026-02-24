class Database:
    def get_user(self, user_id):
        # Simulates a database call
        pass

class UserService:
    def __init__(self, database):
        self.database = database

    def get_user_name(self, user_id):
        user = self.database.get_user(user_id)
        if user:
            return user.get('name')
        return None
