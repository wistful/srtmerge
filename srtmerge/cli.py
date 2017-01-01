#! /usr/bin/env python
# coding:utf-8

"""Command-line interface to merge two subtitle files."""

from chardet.universaldetector import UniversalDetector
import click

from srtmerge import __version__, __release_date__
from srtmerge import common
from srtmerge import reader
from srtmerge import writer


def print_version(ctx, _, value):
    """Print current version to the stdout."""
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version %s (%s).' % (__version__, __release_date__))
    ctx.exit()


def detect_encoding(file_path):
    """Return file encoding."""
    ud = UniversalDetector()
    with open(file_path, 'rb') as fd:
        for line in fd:
            ud.feed(line)
            if ud.done:
                break
        ud.close()
        return ud.result['encoding']


def merge_subtitles(in_path1, in_path2, out_path, encoding):
    """Merge subtitles from two files into third."""
    subs1 = reader.read(in_path1, detect_encoding(in_path1))
    subs2 = reader.read(in_path2, detect_encoding(in_path2))
    writer.write(out_path, common.merge(subs1, subs2), encoding)


@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('--encoding', default='utf8', type=str)
@click.argument('inpath1', type=click.Path(exists=True), required=True)
@click.argument('inpath2', type=click.Path(exists=True), required=True)
@click.argument('outpath', type=click.Path(writable=True), nargs=1)
def main(encoding, inpath1, inpath2, outpath):
    """Entry point for the CLI."""
    merge_subtitles(inpath1, inpath2, outpath, encoding)
