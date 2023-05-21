from django import forms


class InputSiteForm(forms.Form):
    url = forms.URLField(max_length=300, label="Insert URL to be verified:")
    query = forms.CharField(max_length=100, label="Insert keywords to filter the results: (optional)", required=False)
    search = forms.CharField(max_length=100, label="Insert keywords for search engines: (optional)", required=False)
    user_agent = forms.CharField(max_length=300, label="Insert User Agent info:")
    context = forms.CharField(max_length=100, label="Insert user context: (optional)", required=False)

