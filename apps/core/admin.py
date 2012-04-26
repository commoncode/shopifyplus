


def _strong_readonly_field(field, short_desc, allow_tags=True):
    def wrapped(self, obj):
        attr = getattr(obj, field)
        if attr is not None:
            return '<strong>%s</strong>' % attr
        return ''
    _strong_readonly_field.short_description = short_desc
    _strong_readonly_field.allow_tags = allow_tags
    return wrapped
