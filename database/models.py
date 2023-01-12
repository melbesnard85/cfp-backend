from mongoengine import Document, EmailField, StringField
from flask_bcrypt import generate_password_hash, check_password_hash
import string, random
class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    salt = StringField()
    def hash_password(self):
        chars = string.ascii_letters + string.punctuation
        size = 12
        self.salt = ''.join(random.choice(chars) for x in range(size))
        self.password = generate_password_hash(self.password + self.salt).decode('utf8')
    def check_password(self, password):
        return check_password_hash(self.password, password + self.salt)