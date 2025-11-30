def safe_divide(numerator, denominator):
    """
    Safely divide two numbers with error handling for:
    - Non-numeric inputs
    - Division by zero
    """

    # Convert inputs to numeric values
    try:
        num = float(numerator)
        den = float(denominator)
    except ValueError:
        return "Error: Please enter numeric values only."

    # Perform safe division
    try:
        result = num / den
        return f"The result of the division is {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
