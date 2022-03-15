from django import forms
from django.core.validators import MinValueValidator
from .models import Listing, Category
from datetime import datetime


class ListingForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=200, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label=None, required=False)
    image_url = forms.URLField(required=False, label="Image url (optional)", )
    starting_bid = forms.FloatField(validators=[MinValueValidator(0.01)])
    ending_time = forms.DateTimeField(
        input_formats="%Y-%m-%d %H:%M", initial=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    class Meta:
        model = Listing
        fields = ["title", "description", "category",
                  "image_url", "ending_time"]

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            field = field.field

            field.widget.attrs.update({"class": "form-control"})


class SearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False)
    title = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            field = field.field

            field.widget.attrs.update({"class": "form-control"})
