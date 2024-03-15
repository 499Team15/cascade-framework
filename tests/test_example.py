def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_string():
    assert add("Hello, ", "world!") == "Hello, world!"

def test_add_float():
    assert add(1.5, 2.7) == 4.2
    assert add(0.1, 0.2) == 0.30000000000000004  # Testing floating-point precision

def test_add_negative():
    assert add(-5, -7) == -12
    assert add(-3, 5) == 2

def test_add_large_numbers():
    assert add(1000000, 2000000) == 3000000
    assert add(9999999999, 1) == 10000000000