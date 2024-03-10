#!/usr/bin/env python3

import os
import shutil
import subprocess

from pathlib import Path


import click

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
            if entry.is_dir():
                shutil.copytree(entry, output_dir / entry.name)
            else:
                shutil.copyfile(entry, output_dir / entry.name)

    for document_path in src_dir.iterdir():
        if document_path.name.startswith('_') or document_path.name.startswith('.') or document_path.is_dir():
            continue

        title = document_path.name.replace('.md', '')
        output_file_name = f'{title}.html'
        subprocess.run(['pandoc', str(document_path), '--from=gfm', '--to=html', '--standalone',
                        f'--metadata=title:{title}', f'--resource-path={output_dir}',
                        f'--include-in-header=_pandoc_head.html',
                        f'--include-before-body=_pandoc_header.html',
                        f'--include-after-body=_pandoc_footer.html',
                        '--css=_static/github-markdown.css', '--css=_static/custom.css',
                        f'--output={output_dir / output_file_name}'], shell=True)


if __name__ == '__main__':
    compile_markdown()
