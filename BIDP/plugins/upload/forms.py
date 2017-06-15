from django import forms
from django.core.urlresolvers import reverse

class UploadProjectForm(forms.Form):
    legend = "Upload Project"
    operation_type = forms.CharField(
        initial = "Upload Project",
        widget = forms.HiddenInput()
    )
    project_name = forms.CharField(
        label = "New Project Name",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "required",
                "data-bv-notempty": "true",
                "data-bv-notempty-message": "Project name is required"
            }
        )
    )
    project_description = forms.CharField(
        label = "New Project Description",
        widget = forms.Textarea(
            attrs = {
                "rows": "5",
                "class": "form-control",
                "placeholder": "required",
                "data-bv-notempty": "true",
                "data-bv-notempty-message": "Project Description is required"
            }
        )
    )
    upload_file = forms.FileField(
        required = False,
        label = "Project File",
        help_text = "Select a json file to upload or you will create an empty project",
        widget = forms.FileInput(
            attrs = {
                "data-bv-file": "true",
                "data-bv-file-extension": "json",
                "data-bv-file-type": "text/plain"
            }
        )
    )
    submit = "Upload"
    
class UploadSampleForm(forms.Form):
    legend = "Upload Sample"
    operation_type = forms.CharField(
        initial = "Upload Sample",
        widget = forms.HiddenInput()
    )
    project_name = forms.CharField(
        widget = forms.HiddenInput()
    )
    upload_file = forms.FileField(
        label = "Sample File",
        help_text = 'Select a sample json file to upload',
        widget = forms.FileInput(
            attrs = {
                "data-bv-file": "true",
                "data-bv-file-extension": "json",
                "data-bv-file-type": "text/plain"
            }
        )
    )
    submit = "Upload"
