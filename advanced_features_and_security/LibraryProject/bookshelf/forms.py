from django import forms

class ExampleForm(forms.Form):
    q = forms.CharField(label="Search", max_length=100, required=False)
    author = forms.CharField(max_length=100, required=False)
    order = forms.ChoiceField(
        required=False,
        choices=[
            ("title", "Title A–Z"),
            ("-title", "Title Z–A"),
            ("author__name", "Author A–Z"),
            ("-author__name", "Author Z–A"),
        ],
    )

    def clean_q(self):
        # normalize/strip (you could also reject unexpected chars with a regex)
        return (self.cleaned_data["q"] or "").strip()
