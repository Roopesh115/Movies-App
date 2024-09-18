from . models import Movie
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'desc', 'year', 'img', 'actors', 'categories', 'trailer']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter movie title'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter movie description'})
        self.fields['year'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter release year'})
        self.fields['img'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['actors'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter actors'})
        self.fields['categories'].widget.attrs.update({'class': 'form-control'})
        self.fields['trailer'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter YouTube trailer link'})

