from os.path import dirname, join, exists, basename, splitext
from tempfile import mkdtemp, gettempdir

import jinja2
import subprocess

from shutil import rmtree, copy2

import os

from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError


class PdfCreator:
    def __init__(self, temp_directory=None):
        """
        :param temp_directory: Directory, where temporary directory needed for generating pdf will be created.
        If no directory is specified, then directory will be created in platform temporary directory. For example in
        '/tmp' on Linux.
        """
        self._env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader('/')
        )
        if temp_directory is None:
            self.tmp_dir_placement = gettempdir()
        else:
            self.tmp_dir_placement = temp_directory

    def generate_pdf(self, pdf_creating_dto: PdfCreatingDto):
        self.check_dto(pdf_creating_dto)
        directory, file = self.get_output_dir_and_file(pdf_creating_dto.output_file)
        tmp_dir = mkdtemp(dir=self.tmp_dir_placement)
        try:
            template = self._env.get_template(pdf_creating_dto.template)
            output = template.render(pdf_creating_dto.keys_for_template)
            processed_template = join(tmp_dir, 'processed_template.tex')
            with open(processed_template, 'w') as f:
                f.write(output)
            with open(os.devnull, 'w') as null_output:  # redirect stdout and stderr output from pdflatex to /dev/null
                completed = subprocess.run(['pdflatex', '-interaction', 'nonstopmode', '-output-directory',
                                            tmp_dir, '-jobname', file, processed_template], stdout=null_output,
                                           stderr=null_output)
            if completed.returncode != 0:
                raise PdfCreatingError('Failed LaTeX compilation when generating ' + pdf_creating_dto.output_file)
            copy2(join(tmp_dir, file + '.pdf'), pdf_creating_dto.output_file)
            if not exists(pdf_creating_dto.output_file):
                raise PdfCreatingError('An error occurred while copying ' + pdf_creating_dto.output_file)
        finally:
            if exists(tmp_dir):
                rmtree(tmp_dir)

    def check_dto(self, pdf_creating_dto: PdfCreatingDto):
        if pdf_creating_dto.template is None:
            raise TypeError('Template specified is None')
        if not exists(pdf_creating_dto.template):
            raise ValueError('Given template (' + pdf_creating_dto.template + ') does no exists')
        if pdf_creating_dto.output_file is None:
            raise TypeError('Output file is None')
        directory = dirname(pdf_creating_dto.output_file)
        if not exists(directory):
            raise ValueError('Directory ' + directory + ' for output file does not exists')

    def get_output_dir_and_file(self, file_name):
        directory = dirname(file_name)
        file = basename(file_name)
        f, ext = splitext(file)
        if ext == '' or ext == '.pdf':
            return directory, f
        else:
            return directory, file
