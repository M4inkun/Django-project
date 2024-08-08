menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'Add page', 'url_name': 'addpage'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Log in', 'url_name': 'login'},
        ]


class DataMixin:
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
