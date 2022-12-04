from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ConteudoForm, PostSearchForm
from .models import Conteudo, Categoria
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
class HomeView(ListView):
    model = Conteudo
    template_name = 'home.html'
    ordering = ['-post_data']
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        cat_menu = Categoria.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoriaView(request, cats):
    category_posts = Conteudo.objects.filter(categoria=cats)
    return render(request, 'categoria.html', 
  		  {'cats':cats, 'category_posts':category_posts})

def CategoriaListView(request):
    cat_menu_list = Categoria.objects.all()
    return render(request, 'categoria_list.html', {'cat_menu_list': cat_menu_list})

class PostagemView(DetailView):
    model = Conteudo
    template_name = 'post_details.html'

class AdicionarPostView(CreateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'adicionar_posts.html'

class AtualizarPostView(UpdateView):
    model = Conteudo
    template_name = 'atualizar_post.html'
    fields = ['titulo', 'corpo']

class DeletePostView(DeleteView):
    model = Conteudo
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

def PostSearchView(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(categoria=c)
            if q is not None:
                query &= Q(titulo__contains=q)

            results = Conteudo.objects.filter(query)

    return render(request, 'search.html',
                  {'form': form,
                   'q': q,
                   'results': results})
    