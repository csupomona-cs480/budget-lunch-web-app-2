import unittest

def is_prime_number(num):
    if num <= 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


class TestHelloWorld(unittest.TestCase):
    def test_is_prime_number(self):
        self.assertEqual(is_prime_number(11), True)
        self.assertEqual(is_prime_number(12), False)
        self.assertEqual(is_prime_number(14), False)
        self.assertEqual(is_prime_number(22), False)
        self.assertEqual(is_prime_number(23), True)
        self.assertEqual(is_prime_number(24), False)

if __name__ == "__main__":
    unittest.main()