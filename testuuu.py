# test_hello.py
import unittest

# hello.py
def say_hello(name):
    return f"Hellfo, {name}!"

class TestHello(unittest.TestCase):
    def test_say_hello(self):
        self.assertEqual(say_hello("World"), "Hello, World!")

if __name__ == "__main__":
    unittest.main()