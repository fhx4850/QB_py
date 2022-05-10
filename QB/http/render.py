from jinja2 import Environment, FileSystemLoader
import QB.settings as settings


class HtmlRender:
    """HTML rendering logic."""

    def __init__(self, template_path: str, template_data=None):
        self.template_path = template_path
        self.template_data = template_data
        self.templ_path, self.templ_name = self._create_template_path(self.template_path)
        self.env = Environment(loader=FileSystemLoader(self.templ_path))

    def render(self):
        """Template rendering with jinja."""
        templ = self.env.get_template(self.templ_name)

        data = self.template_data

        template = templ.render(data)
        return template

    def _create_template_path(self, path):
        """Getting path, name."""
        parse_path = path.split('\\')
        template_path = ''
        template_name = parse_path[-1]
        for i in parse_path[:-1]:
            template_path += i + '/'
        return template_path, template_name

    def add_template_func(self, func):
        """Adding jinja function."""
        self.env.globals[func.__name__] = func