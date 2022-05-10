# import sys, os
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from QB.http.render import HtmlRender


def index():
    ren = HtmlRender('templates\index.html', {'test': "hello"})
    ren.add_template_func(hi)
    return ren.render()

def hi():
    return 'hello'