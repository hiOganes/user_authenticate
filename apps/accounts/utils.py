from time import sleep
from string import digits, ascii_letters
from random import choices, shuffle


def send_sms(phone_number: str, code: str) -> None:
    'simulates sending code via SMS'
    sleep(2)
    return None


def create_sms_code() -> str:
    'creates a code for SMS'
    return ''.join(choices(digits, k=4))


def generate_invite_code() -> str:
    'generates an invitation code'
    numbers = choices(digits, k=3)
    letters = choices(ascii_letters, k=3)
    union_symbols = numbers + letters
    shuffle(union_symbols)
    return ''.join(union_symbols)