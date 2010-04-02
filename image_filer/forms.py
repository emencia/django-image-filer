from django import forms
from image_filer.models import Folder

class NewFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name', )


class ImageExportForm(forms.Form):
    FORMAT_CHOICES = (
        ('jpg', 'jpg'),
        ('png', 'png'),
        ('gif', 'gif'),
    )
    format = forms.ChoiceField(choices=FORMAT_CHOICES)

    crop = forms.BooleanField(required=False)
    upscale = forms.BooleanField(required=False)

    width = forms.IntegerField()
    height = forms.IntegerField()
