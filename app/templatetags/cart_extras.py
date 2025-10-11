from django import template

register = template.Library()

@register.filter
def multiply(qty, price):
    return qty * price

@register.filter
def calc_total(orders):
    return sum([o.quantity * o.product.selling_price for o in orders])
