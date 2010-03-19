#!/usr/bin/env python
import os
import optparse

from librarian import html


if __name__ == '__main__':
    # Parse commandline arguments
    usage = """Usage: %prog [options] SOURCE [SOURCE...]
    Extract theme fragments from SOURCE."""
    
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
        help='print status messages to stdout')
    
    options, input_filenames = parser.parse_args()
    
    if len(input_filenames) < 1:
        parser.print_help()
        exit(1)
    
    # Do some real work
    for input_filename in input_filenames:
        if options.verbose:
            print input_filename
    
        output_filename = os.path.splitext(input_filename)[0] + '.fragments.html'
    
        closed_fragments, open_fragments = html.extract_fragments(input_filename)

        for fragment_id in open_fragments:
            print '%s:warning:unclosed fragment #%s' % (input_filename, fragment_id)

        output_file = open(output_filename, 'w')
        output_file.write("""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
            <html><head>
                <title>bookfragments output</title>
                <meta http-equiv="content-type" content="text/html;charset=utf-8"/>
                <link rel="stylesheet" href="master.css" type="text/css" media="screen" charset="utf-8" />
            </head>
            <body>""")
        for fragment in closed_fragments.values():
            fragment_html = u'<div class="fragment"><h3>[#%s] %s</h3>%s</div>' % (fragment.id, fragment.themes, fragment)
            output_file.write(fragment_html.encode('utf-8'))
        output_file.write('</body></html>')
        output_file.close()

