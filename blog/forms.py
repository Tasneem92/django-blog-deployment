from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text')

    # grabbing a particular field widget
    # widget is an attribute that is a dictionary
        widgets = {
            # keys of the things I wanna edit:
            # TextInput is a widget
            # textinputclass and post content are my own classes
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            # connecting text attribute (our text in the blog post form) to these CSS classes
            'text':forms.Textarea(attrs={'class':'editable medium-editors-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author','text')
 
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editors-textarea'})
        }
