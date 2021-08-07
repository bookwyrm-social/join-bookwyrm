""" generate html files """
from jinja2 import Environment, FileSystemLoader

paths = [
    "index.html",
    "instances/index.html"
]

env = Environment(
    loader=FileSystemLoader("templates/")
)
for path in paths:
    print("Generating", path)
    template_string = open(f"templates/{path}", 'r').read()
    template = env.from_string(template_string)

    with open(f"site/{path}", "w") as render_file:
        render_file.write(template.render())
