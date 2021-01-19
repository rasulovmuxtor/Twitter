from django.forms import ModelForm,Form
from .models import Post, Comment
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('poster','created')
        widgets={
            'content':forms.Textarea(attrs={
                'placeholder':'New Post',
                'class':'form-control',
                'rows':"7",
                'maxlength':'280',
            })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('poster','created','post')
        widgets={
            'content':forms.Textarea(attrs={
                'placeholder':'New Comment',
                'class':'form-control',
                'rows':"6",
                'maxlength':'280',
            })
        }


# class TrackerForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(TrackerForm, self).__init__(*args, **kwargs)
#         self.fields.keyOrder = ['date_job_start','date_job_end','description','onsite','billable','client']

