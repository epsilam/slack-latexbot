from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, respond_to
from tempfile import TemporaryDirectory
from slackclient import SlackClient
from subprocess import check_call
from os.path import join
import re

class LatexPlugin(MachineBasePlugin):
    #The MachineBasePlugin class takes 3 arguments on init. We don't really care what they are so we write arg1, etc.
    def __init__(self, arg1, arg2, arg3):
        super().__init__(arg1, arg2, arg3)
        self.sc = SlackClient(self.settings['SLACK_API_TOKEN'])

    def catch_all(self, data):
        if data['type'] == 'message' and type(data['text']) == str:
            # =tex command
            if re.match(r'=tex[\s]', data['text'], re.IGNORECASE):
                self.render_upload_latex(data['text'][5:], data['channel'])
            # =t command
            if re.match(r'=t[\s]', data['text'], re.IGNORECASE):
                self.render_upload_latex('$' + data['text'][3:] + '$', data['channel'])
            # =help command
            if re.match(r'=help', data['text'], re.IGNORECASE):
                self.sc.api_call("chat.postMessage",channel=data['channel'],text=self.settings['HELP_RESPONSE'])

    def render_upload_latex(self, msgtext, msgchannel):
        #Slack converts the characters &, <, and > in user messages to special strings. Here, we convert them back.
        msgtext = msgtext.replace(r'&amp;', r'&')
        msgtext = msgtext.replace(r'&lt;', r'<')
        msgtext = msgtext.replace(r'&gt;', r'>')
        #Replace placeholder variable in LaTeX template with the message text
        template = self.settings['LATEX_TEMPLATE_FILE'].substitute(input_text=msgtext)
        with TemporaryDirectory() as dir:
            try:
                #Create temporary tex file with message body substituted in.
                with open(join(dir, 'outfile.tex'), mode='w') as file:
                    file.write(template)
                #Compile tex file into pdf.
                check_call(['pdflatex', '-halt-on-error', '-no-shell-escape', '-interaction', 'nonstopmode', 'outfile.tex'], cwd=dir, stdout=None, stderr=None)
                #Convert pdf file into png file.
                check_call(['convert', '-density', '200', 'outfile.pdf', '-quality', '90', '-strip', '-background', 'white', '-flatten', 'outfile.png'], cwd=dir, stdout=None, stderr=None)
                #Upload png file via Slack API.
                with open(join(dir, 'outfile.png'), mode='rb') as file_content:
                    self.sc.api_call(
                    "files.upload",
                    channels=msgchannel,
                    file=file_content,
                    title="LaTeX.png"
                    )
            except Exception as error:
                print(error)
                return "Error: invalid LaTeX."
