from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def add(value, arg):
    """Add the argument to the value"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def category_name(counter):
    categories = {
        1: "Men's Clothing",
        2: "Women's Clothing",
        3: "Men's Shoes",
        4: "Women's Shoes"
    }
    return categories.get(counter, "Category")

@register.filter
def men_category(counter):
    categories = {
        1: "Casual Wear",
        2: "Formal Wear",
        3: "Sports Wear"
    }
    return categories.get(counter, "Category") 