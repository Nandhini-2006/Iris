from redactor import redact_pii


text = """
User email: nandhini@example.com
Phone: +91 9876543210
Card: 4111 1111 1111 1111

The application crashes when login() is called.
"""

result = redact_pii(text)

print(result)