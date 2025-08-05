
from secrets import choice
length = 14
def generate():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+=?><''://"
    return "".join(choice(chars) for char in range(length))

