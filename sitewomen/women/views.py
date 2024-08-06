from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, reverse, render
from django.template.defaultfilters import slugify
from women.models import Women, Category, ModelTags, UploadFiles
from women.forms import AddPostForm, UploadFileForm

menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'Add page', 'url_name': 'addpage'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Log in', 'url_name': 'login'},
]


def index(request):
    posts = Women.published.all().select_related('cat')

    data = {'title': 'Main page',
            'menu': menu,
            'posts': posts,
            'cat_selected': 0,
    }

    return render(request, 'women/index.html', context=data)


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


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
            #     Women.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')

    data = {'title': f'Category: {category.name}',
            'menu': menu,
            'posts': posts,
            'cat_selected': category.pk,
            }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(ModelTags, slug=tag_slug)
    posts = tag.tags.filter(is_publisher=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page not found</h1>')
