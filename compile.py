#!/usr/bin/env python3

import os
import shutil
import subprocess
import click

from pathlib import Path


@click.command()
@click.option('--working-directory', type=click.Path(exists=True, file_okay=False, path_type=Path),
              default=Path(os.getcwd()))
def compile_markdown(working_directory: Path):
    src_dir = working_directory / 'src'
    output_dir = working_directory / 'public'

    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir()

    for entry in src_dir.iterdir():
        if entry.name.startswith('_') or entry.name.startswith('.'):
            if entry.is_dir() and not entry.name.startswith('.:'):
                shutil.copytree(entry, output_dir / entry.name)
            else:
                shutil.copyfile(entry, output_dir / entry.name)

    for document_dir in src_dir.iterdir():
        if document_dir.name.startswith('_') or document_dir.name.startswith('.') or document_dir.is_file():
            continue

        readme_files_path = document_dir / 'readme_files'
        current_readme_files_dir_name = f'_{document_dir.name}_{readme_files_path.name}'
        if readme_files_path.exists():
            shutil.copytree(readme_files_path, output_dir / current_readme_files_dir_name)

        title = document_dir.name
        output_file_name = f'{title}.html'
        output_file_path = output_dir / output_file_name
        subprocess.run(['pandoc', str(document_dir / 'README.md'), '--from=gfm', '--to=html', '--standalone', '--mathjax',
                        f'--metadata=title:{title}', f'--resource-path={output_dir}',
                        '--include-in-header=_pandoc_head.html',
                        '--include-before-body=_pandoc_header.html',
                        '--include-after-body=_pandoc_footer.html',
                        '--css=_static/github-markdown.css', '--css=_static/custom.css',
                        f'--output={output_file_path}'])

        html_text = output_file_path.read_text()\
            .replace('readme_files', current_readme_files_dir_name)\
            .replace('../_static', '_static')\
            .replace('../../README.md', '/lab-wdpo')
        output_file_path.write_text(html_text)


if __name__ == '__main__':
    compile_markdown()
