class Category:
    def __init__(self, id, name, icon_path=None, sort_order=1):
        self.id = id
        self.name = name
        self.icon_path = icon_path
        self.sort_order = sort_order

class App:
    def __init__(self, id, name, path, category_id, icon_path=None, bg_color=None, is_square=False):
        self.id = id
        self.name = name
        self.path = path
        self.category_id = category_id
        self.icon_path = icon_path
        self.bg_color = bg_color
        self.is_square = is_square

class Settings:
    def __init__(self, background_image=None, background_color=None, opacity=None, font_family=None, admin_password=None):
        self.background_image = background_image
        self.background_color = background_color
        self.opacity = opacity
        self.font_family = font_family
        self.admin_password = admin_password