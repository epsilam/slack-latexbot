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

HELP_RESPONSE = """
It seems you have asked for help. I have several available commands. Putting a command at the beginning of your message will trigger an action. Here they are:
>`=tex <message>`
When this command is issued, I will compile whatever LaTeX code appears in <message>, and will upload a .png file of the result. Example: `=tex This is an equation: $1\neq 2$`.
>`=t <message>`
This command just takes a single equation as input without delimiters. It just takes whatever is passed through <message>, slaps two $ signs on both ends and then puts that through the same process as the =tex command. Example: `=t 1\neq 2`.
>`=help`
Entering this command will cause me to display this help message.
"""
