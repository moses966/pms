from django import template
register = template.Library()


@register.filter(name='add_commas')
def add_commas(value):
    try:
        # Convert the value to a float or integer and then format it with commas
        value_formatted = "{:,.0f}".format(float(value))
        return value_formatted
    except (TypeError, ValueError):
        # If conversion fails, return the original value
        return value

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 'Not Sure!')

@register.filter(name='capitalize_name')
def capitalize_name(value):
    """
    Capitalize the first letter of each word in a string.
    """
    return ' '.join(word.capitalize() for word in value.split())
