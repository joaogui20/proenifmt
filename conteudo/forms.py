from django import forms
from .models import Conteudo, Categoria

choices = Categoria.objects.all().values_list('nome', 'nome')

choice_list = []

for item in choices:
    choice_list.append(item)

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ('titulo', 'autor', 'corpo', 'categoria', 'imagem', 'arquivo', 'youtube')
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'users_id', 'type': 'hidden'}),
            'corpo': forms.Textarea(attrs={'class': 'form-control'}),
            'youtube': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PostSearchForm(forms.Form):
    q = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Pesquisar por'
        self.fields['q'].widget.attrs.update({'class': 'form-control'})