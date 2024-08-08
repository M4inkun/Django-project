from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, reverse, render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from women.models import Women, Category, ModelTags, UploadFiles
from women.forms import AddPostForm, UploadFileForm

menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'Add page', 'url_name': 'addpage'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Log in', 'url_name': 'login'},
]


# def index(request):
#     posts = Women.published.all().select_related('cat')
#
#     data = {
#         'title': 'Main page',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=data)


class WomenHome(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Main page',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

# def handle_uploaded_file(f):
#     with open(f"sitewomen/uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'About site', 'menu': menu, 'form': form})


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])



# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse(f'Contact\'s page')


def login(request):
    return HttpResponse(f'Login\'s page')


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {'title': f'Category: {category.name}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': category.pk,
#             }
#     return render(request, 'women/index.html', context=data)


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(ModelTags, slug=tag_slug)
#     posts = tag.tags.filter(is_publisher=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Tag: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)


class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = ModelTags.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег:' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tag__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page not found</h1>')
