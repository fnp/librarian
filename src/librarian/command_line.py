import argparse
import os.path
from .builders import builders
from .document import WLDocument


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(description="PARSER DESCRIPTION")

    parser.add_argument(
        'builder',
        choices=builders.keys(),
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

    # Specific 
    parser.add_argument(
        '-b', '--base-url', metavar="URL",
        help="Base for relative URLs in documents (like image sources)"
    )

    parser.add_argument(
        '--mp3',
        metavar="FILE",
        nargs="*",
        help='specifies an MP3 file, if needed'
    )

    args = parser.parse_args()
    builder = builders[args.builder]

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

    builder = builders[args.builder]
    kwargs = {
        "mp3": args.mp3,
    }

    output = document.build(builder, **kwargs)
    with open(output_file_path, 'wb') as f:
        f.write(output.get_bytes())
