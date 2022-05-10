from myproject.views import index


url_path = [
    {'path': '/', 'handler': index, 'name': 'index'},
    {'path': '/index/', 'handler': index, 'name': 'index'},
]
