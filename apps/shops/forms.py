from django import forms

class ShopForm(forms.ModelForm):
    """
    Subclass Pinax's Login form to change a few things.
    """
    
    def clean(self):
        
        # import ipdb; ipdb.set_trace()
        raise forms.ValidationError("This account is currently inactive.")
        # ct = ContentType.objects.get_for_model(self)
        # if len(ct.model_class().objects.all()) > 0:
        #     raise ValidationError(u'Only one template allowed')
                        