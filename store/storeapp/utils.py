
main_menu = [
    {'title': "Каталог", 'url_name': 'cat'},
]

main_menu_right = [{'title': "Корзина", 'url_name': 'basket_detail'}]

menu_moderators= [
   {'title': "Добавить товар", 'url_name': 'add_product_page'},]


class DataMixin:
    def get_user_context(self,**kwargs):
        context = kwargs

        user_menu = main_menu_right.copy()
        menu_mod_copy = menu_moderators.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(0)
        if not self.request.user.groups.filter(name='staff').exists():
           menu_mod_copy.clear()
        context['menu_mod'] = menu_mod_copy
        context['menu'] = main_menu
        context['menu_right'] = user_menu
        return context
