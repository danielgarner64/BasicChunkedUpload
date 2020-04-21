from django import forms

from uploadDownloadApp.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name',
                  'description',
                  'file',
                  'author'
                  ]
        # Hide fields from user
        widgets = {
                    'author': forms.HiddenInput(),
                    "file_name": forms.HiddenInput(),
                    #"file": forms.FileInput(attrs={"class": "custom-file-input", "type": "file"}),
                  }
        labels = {
            "file": "Select and Upload File"
        }

