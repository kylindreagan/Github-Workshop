def is_div_8(a):
    return a % 8 == 0

def get_count(n):
    if not isinstance(n, int):
        raise ValueError("Uncountable")
    c = 0
    n = abs(n)
    while n > 0:
        n -= 1
        c += 1
    return c

def get_degrees(sides):
    if sides < 3:
        raise ValueError("Invalid shape")
    return ((sides-2)*180)

def might_be_prime(n):
    if isinstance(n, int):
        return True
    else:
        return False

def sum_2(a,b):
    return a + b