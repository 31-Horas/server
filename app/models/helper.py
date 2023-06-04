import bcrypt
import random

def encryptPassword(password):
    """Encrypt the password using bcrypt."""
    salt = bcrypt.gensalt(10)
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashedPassword.decode('utf-8')

def matchPassword(password, savedPassword):
    """Check if the provided password matches the saved password using bcrypt."""
    return bcrypt.checkpw(password.encode('utf-8'), savedPassword.encode('utf-8'))

def generateRandomNumberCode(length):
    """Generate a random number code of the specified length."""
    size_digits = 10 ** (length - 1)
    return random.randint(1 * size_digits, 9 * size_digits)
