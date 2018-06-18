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

    @listen_to(r"^=tex ", re.IGNORECASE)
    def respond_tex(self, msg):
        self.render_upload_latex(msg.text[5:], str(msg.channel.id))

    @listen_to(r"^=t ", re.IGNORECASE)
    def respond_quicktex(self, msg):
        self.render_upload_latex('$' + msg.text[3:] + '$', str(msg.channel.id))

    @respond_to(r"help", re.IGNORECASE)
    def help_response(self, msg):
        response = """
It seems you have asked for help. I have several available commands. Putting a command at the beginning of your message will trigger an action. Here they are:
> =tex <message>
This command will compile whatever LaTeX code appears in <message>, and will upload a .png file of the result.
> =t <message>
Quick LaTeX: just takes a single equation as input without delimiters.
        """
        msg.reply(response)

    #> =inline <message>
    #This command will only render the parts of your message which come between the $ delimiters. One .png image will be rendered for each pair of delimiters.

    #@listen_to(r"^=inline ", re.IGNORECASE)
    #def respond_inline(self, msg):
    #    if
    #    tex_list = re.findall(r"\[;([\w\W]+);\]", msg.text[7:])
    #    for item in tex_list:
    #        message = "$" + item + "$"
    #        self.render_upload_latex(msg.text, str(msg.channel.id))
