#=== Required for slack-machine to work
SLACK_API_TOKEN = 'your-token-here'
PLUGINS = [
    'plugins.latex.LatexPlugin'
]

#=== Required for latex plugin to work
from string import Template
with open('latex.tex',mode='r') as templatefile:
    template = Template(templatefile.read())
LATEX_TEMPLATE_FILE = template
