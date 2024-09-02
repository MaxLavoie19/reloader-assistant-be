class UserExists(Exception):
    def __init__(self):
        super(Exception).__init__('User already exists')
