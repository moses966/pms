from django import template
register = template.Library()

@register.filter(name='format_salary')
def format_salary(value):
    """
    Formats the salary value with commas after every three digits.
    """
    try:
        # Attempt to convert value to float
        salary = float(value)
        # Format the salary as a float with two decimal places
        return "{:,.2f}".format(salary)
    except (ValueError, TypeError):
        # If conversion fails, return the original value
        return value
