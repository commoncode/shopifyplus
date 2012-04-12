from django import template

register = template.Library()

@register.filter
def currency_filter(value, zero_allowed):

	if value is not None:
	
		if value > 0 or bool(zero_allowed):
			return "$%.2f" % (value)
		else: return None
	
	else:
		return value



