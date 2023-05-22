from random import randint

def gen_int_without_repeats(num: int, minimum: int, maximum: int) -> int:
    """A function that generates a random integer that is NOT equal to `num`."""
    while True:
        random = randint(minimum, maximum)
        if random != num:
            return random
        