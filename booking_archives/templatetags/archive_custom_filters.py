from django import template
import calendar

register = template.Library()

@register.filter(name='month_name')
def month_name(month_number):
    return calendar.month_name[month_number]


@register.filter(name='shillings_in_words')
def shillings_in_words(amount):
    amount = int(amount)  # Convert to integer to handle Decimal values

    if amount <= 0:
        return "Zero Shillings"

    units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

    def num_to_words(num):
        if num < 10:
            return units[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            return tens[num // 10] + ('' if num % 10 == 0 else ' ' + units[num % 10])
        elif num < 1000:
            return units[num // 100] + ' Hundred' + ('' if num % 100 == 0 else ' and ' + num_to_words(num % 100))
        elif num < 1000000:
            return num_to_words(num // 1000) + ' Thousand' + ('' if num % 1000 == 0 else ' ' + num_to_words(num % 1000))
        elif num < 1000000000:
            return num_to_words(num // 1000000) + ' Million' + ('' if num % 1000000 == 0 else ' ' + num_to_words(num % 1000000))

    words = num_to_words(amount)
    return f"{words} Shillings"
