letter_x = 5

def f(x: int) -> int:
    return x * 2

if letter_x == 5:
    letter_x = f(letter_x)
else:
    letter_x = f(letter_x) / 4
print(letter_x)
