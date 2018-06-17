from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
from tempfile import TemporaryDirectory
from slackclient import SlackClient
from subprocess import check_call
from os.path import join
import re

class LatexPlugin(MachineBasePlugin):

    @listen_to(r"^=tex", re.IGNORECASE)
    def render_latex(self, msg):
        template = self.settings['LATEX_TEMPLATE_FILE'].substitute(input_text=msg.text[4:])
        with TemporaryDirectory() as dir:
            #Create temporary tex file with message body substituted in.
            with open(join(dir, 'outfile.tex'), mode='w') as file:
                file.write(template)
            #Compile tex file into pdf.
            check_call(['pdflatex', '-halt-on-error', 'outfile.tex'], cwd=dir, stdout=None, stderr=None)
            #Convert pdf file into png file.
            check_call(['convert', '-density', '200', 'outfile.pdf', '-quality', '90', '-strip', 'outfile.png'], cwd=dir, stdout=None, stderr=None)
            #Upload png file via Slack API.
            sc = SlackClient(self.settings['SLACK_API_TOKEN'])
            with open(join(dir, 'outfile.png'), mode='rb') as file_content:
                sc.api_call(
                    "files.upload",
                    channels=str(msg.channel.id),
                    file=file_content,
                    title="LaTeX.png"
                )
