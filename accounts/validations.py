from django import forms


# Validation for username
def clean_username(username):
    if len(username) < 2:
        raise forms.ValidationError("Username must be at least 2 characters long.")
    return username

# Validation for password complexity
def clean_password(password):
    if len(password) < 6:
        raise forms.ValidationError("Password must be at least 6 characters long.")
    # Add more requirements as needed
    return password

# Validation for phone number (numeric)
def clean_phone_number(phone_number):
    if not phone_number.isdigit() or len(phone_number) < 8:
        raise forms.ValidationError("Phone number must contain only numeric digits and must be at least 8 characters long.")
    return phone_number

# Validation for first name (string)
def clean_first_name(first_name):
    if not first_name.isalpha():
        raise forms.ValidationError("First name must contain only alphabets.")
    return first_name

# Validation for last name (string)
def clean_last_name(last_name):
    if not last_name.isalpha():
        raise forms.ValidationError("Last name must contain only alphabets.")
    return last_name
