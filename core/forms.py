# vim: ts=4 sw=4 et fdm=indent
import floppyforms.__future__ as forms

from .models import Hero, Campaign, CampaignHero


class PlaceholderMixin(object):
    def __init__(self, *args, **kwargs):
        super(PlaceholderMixin, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
                isinstance(field.widget, forms.Textarea) or \
                isinstance(field.widget, forms.DateInput) or \
                isinstance(field.widget, forms.DateTimeInput) or \
                isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({'placeholder': field.help_text})
                field.help_text = ''

class CampaignForm(PlaceholderMixin, forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('name', 'slug', 'description', 'location_address', 'threshold')
        widgets = {
            "slug": forms.TextInput(attrs={"data-slug-from": "name"}),
        }


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ('email', 'username', 'photo', 'superpowers')


class RegistrationForm(HeroForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), 
                                label="Confirm password")

    class Meta:
        model = Hero
        fields = ('username', 'email', 'photo', 'password', 'password2', 'superpowers')
        widgets = {
            'superpowers': forms.CheckboxSelectMultiple()
        }

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(HeroForm, self).save(commit=False)
        if self.cleaned_data.get('password', False):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CampaignJoinForm(forms.ModelForm):
    class Meta:
        model = CampaignHero
        fields = ('public',)


class CampaignOwnForm(forms.Form):
    agree_terms = forms.BooleanField()
