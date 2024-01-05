def starts_with_hello(string):
    if string.startswith("Hello"):
        return True
    else:
        return False

# Example usage
print(starts_with_hello("Hello, world!"))  # Output: True
print(starts_with_hello("Hi there!"))      # Output: False
