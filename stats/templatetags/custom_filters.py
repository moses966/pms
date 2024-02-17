from django import template
register = template.Library()

@register.filter(name='format_salary')
def format_salary(value):
    """
    Formats the salary value with commas after every three digits.
    """
    if value is not None:
        return "{:,.2f}".format(value)
    return value
