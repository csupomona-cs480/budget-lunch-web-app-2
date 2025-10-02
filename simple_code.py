
def is_prime_number(num):
    if num <= 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


# print(is_prime_number(11)) # True
# print(is_prime_number(12)) # False

try:
    if is_prime_number(11) == True:
        print("Correct!");
    else:
        raise Exception("Incorrect!");

    if is_prime_number(12) == False:
        print("Correct!");
    else:
        raise Exception("Incorrect!");

    print("All tests have passed!");
except Exception as e:
    print(e);
    print("Some test have failed!");

