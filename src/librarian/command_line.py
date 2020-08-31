import argparse
import os.path
from .builders import builders
from .document import WLDocument


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(description="PARSER DESCRIPTION")

    parser.add_argument(
        'builder',
        choices=[b.identifier for b in builders],
        help="Builder"
    )
    parser.add_argument('input_file')
    parser.add_argument(
        '-o', '--output-file', metavar='FILE',
        help='specifies the output file'
    )
    parser.add_argument(
        '-O', '--output-dir', metavar='DIR',
        help='specifies the directory for output'
    )

    args = parser.parse_args()

    if args.output_file:
        output_file_path = args.output_file
    else:
        output_file_path = '.'.join((
            os.path.splitext(args.input_file)[0],
            builder.file_extension
        ))
        if args.output_dir:
            output_file_path = '/'.join((
                args.output_dir,
                output_file_path.rsplit('/', 1)[-1]
            ))

    document = WLDocument(filename=args.input_file)
    output = document.build(args.builder)
    with open(output_file_path, 'wb') as f:
        f.write(output.get_bytes())
