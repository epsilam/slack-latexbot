from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, respond_to
from tempfile import TemporaryDirectory
from slackclient import SlackClient
from subprocess import check_call
from os.path import join
import re

class LatexPlugin(MachineBasePlugin):

    def render_upload_latex(self, msgtext, msgchannel):
        template = self.settings['LATEX_TEMPLATE_FILE'].substitute(input_text=msgtext)
        with TemporaryDirectory() as dir:
            try:
                #Create temporary tex file with message body substituted in.
                with open(join(dir, 'outfile.tex'), mode='w') as file:
                    file.write(template)
                #Compile tex file into pdf.
                check_call(['pdflatex', '-halt-on-error', '-no-shell-escape', '-interaction', 'nonstopmode', 'outfile.tex'], cwd=dir, stdout=None, stderr=None)
                #Convert pdf file into png file.
                check_call(['convert', '-density', '200', 'outfile.pdf', '-quality', '90', '-strip', 'outfile.png'], cwd=dir, stdout=None, stderr=None)
                #Upload png file via Slack API.
                sc = SlackClient(self.settings['SLACK_API_TOKEN'])
                with open(join(dir, 'outfile.png'), mode='rb') as file_content:
                    sc.api_call(
                    "files.upload",
                    channels=msgchannel,
                    file=file_content,
                    title="LaTeX.png"
                    )
            except Exception as error:
                print(error)
                return "Error: invalid LaTeX."

    @listen_to(r"^=tex", re.IGNORECASE)
    def respond_tex(self, msg):
        self.render_upload_latex(msg.text[4:], str(msg.channel.id))

    @listen_to(r"^=t", re.IGNORECASE)
    def respond_quicktex(self, msg):
        self.render_upload_latex('$' + msg.text[2:] + '$', str(msg.channel.id))

    def help_response(self, msg):
        response = r"""
It seems you have asked for help. I have several available commands. Putting a command at the beginning of your message will trigger an action. Here they are:
>`=tex <message>`
When this command is issued, I will compile whatever LaTeX code appears in <message>, and will upload a .png file of the result. Example: `=tex This is an equation: $1\neq 2$`.
>`=t <message>``
This command just takes a single equation as input without delimiters. It just takes whatever is passed through <message>, slaps two $ signs on both ends and then puts that through the same process as the =tex command. Example: `=t 1\neq 2`.
>`=help`
Entering this command will cause me to display this help message. Alternatively, you can @ me and include any uppercase/lowercase variation of the word "help" anywhere in your message.
        """
        msg.say(response)

    @respond_to(r"help", re.IGNORECASE)
    def respond_help_at(self, msg):
        self.help_response(msg)

    @listen_to(r"^=help", re.IGNORECASE)
    def respond_help_command(self, msg):
        self.help_response(msg)
