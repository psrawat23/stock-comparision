from django import forms

class StockSelectionForm(forms.Form):
    stocks = forms.MultipleChoiceField(
        choices=[],  # Set as an empty list initially
        widget=forms.CheckboxSelectMultiple,
        label="Select Stocks"
    )

    def __init__(self, *args, **kwargs):
        stock_choices = kwargs.pop('stock_choices', [])  # Extract the dynamic choices
        super(StockSelectionForm, self).__init__(*args, **kwargs)
        self.fields['stocks'].choices = stock_choices  # Assign the dynamic choices
