import re
import textwrap
from unittest import mock

from stograde.formatters.format_type import FormatType
from stograde.formatters.html import format_file_contents, format_file_compilation, \
    format_file_tests, format_file, format_warnings, format_header, format_files_list, format_assignment_html, \
    format_as_code, format_as_ul
from stograde.formatters.html_template import add_styling
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.process_file.file_result import FileResult
from test.formatters.results_for_tests import compile_results, test_results, file_results


# ----------------------------- add_styling -----------------------------

def test_add_styling():
    formatted = add_styling(assignment='lab1',
                            students=['student4'],
                            content=format_assignment_html(RecordResult(spec_id='lab1',
                                                                        student='student4',
                                                                        first_submission='4/14/2020 16:04:05',
                                                                        warnings=SubmissionWarnings(),
                                                                        file_results=file_results)).content)

    assert formatted == textwrap.dedent('''
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <!--
            Based on:
            Nameless Geometry by nodethirtythree + Templated.org
            http://templated.org/ | @templatedorg
            Released under the Creative Commons Attribution 3.0 License.

            Note from the author: These templates take quite a bit of time to conceive,
            design, and finally code. So please, support our efforts by respecting our
            license: keep our footer credit links intact so people can find out about us
            and what we do. It's the right thing to do, and we'll love you for it :)
        -->
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
            <meta name="keywords" content="" />
            <meta name="description" content="" />
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />
            <title>lab1</title>
            <link href="http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz" rel="stylesheet" type="text/css" />
            <style>
                /*
                    Based on:
                    Nameless Geometry by nodethirtythree + Templated.org
                    http://templated.org/ | @templatedorg
                    Released under the Creative Commons Attribution 3.0 License.

                    Note from the author: These templates take quite a bit of time to conceive,
                    design, and finally code. So please, support our efforts by respecting our
                    license: keep our footer credit links intact so people can find out about us
                    and what we do. It's the right thing to do, and we'll love you for it :)
                */

                * {
                    margin: 0;
                    padding: 0;
                }

                a {
                    color: #cfcfcf;
                    text-decoration: underline;
                }

                a:hover {
                    text-decoration: none;
                }

                body {
                    background: #1f1f1f;
                    color: #909090;
                    font-family: 'Trebuchet MS', sans-serif;
                    font-size: 11pt;
                    line-height: 1.5em;
                }

                strong {
                    color: #cfcfcf;
                }

                br.clear {
                    clear: both;
                }

                h1, h2, h3, h4 {
                    color: #eaeaea;
                    font-weight: normal;
                    margin-bottom: 1em;
                    text-shadow: 0 2px 1px #181818;
                }

                h2, h3, h4 {
                    color: #ffffff;
                    font-family: 'Yanone Kaffeesatz', sans-serif;
                    font-size: 1.5em;
                }

                hr {
                    margin-bottom: 20px;
                }

                img {
                    border-bottom: solid 2px #1c1c1c;
                }

                img.left {
                    float: left;
                    margin: 4px 20px 20px 0;
                }

                img.top {
                    margin: 4px 0 20px 0;
                }

                p {
                    margin-bottom: 1.25em;
                }

                pre {
                    background: #111111;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    overflow: auto;
                    padding-left: 2%;
                }

                ul {
                    margin-bottom: 3em;
                }

                #banner {
                    background: #ffffff;
                }

                #box1 {
                    margin: 0 0 28px 0;
                    overflow: hidden;
                    width: 556px;
                }

                #box2 {
                    float: left;
                    overflow: hidden;
                    width: 264px;
                }

                #box3 {
                    margin: 0 0 0 292px;
                    overflow: hidden;
                    width: 264px;
                }

                #content {
                    margin: 0 0 0 280px;
                    padding: 0;
                    width: 556px;
                }

                #copyright {
                    color: #404040;
                    padding: 8px 0 80px 0;
                    text-align: center;
                    text-shadow: 0 1px 0 #101010;
                }

                #copyright a {
                    color: #404040;
                }

                #footer {
                    color: #808080;
                    margin-top: 16px;
                    padding: 32px;
                    position: relative;
                    text-shadow: 0 1px 0 #000000;
                    width: 1116px;
                }

                #footer a {
                    color: #a0a0a0;
                }

                #footer h2, #footer h3, #footer h4 {
                    color: #ffffff;
                }

                #footer p {
                    margin-bottom: 0;
                }

                #footer ul {
                    list-style: none;
                    margin-bottom: 0;
                }

                #footer ul li {
                    border-bottom: solid 1px #101010;
                    border-top: solid 1px #353535;
                    padding: 16px 0 16px 0;
                }

                #footer ul li.first {
                    border-top: 0;
                    padding-top: 0;
                }

                #footer ul li.last {
                    border-bottom: 0;
                    padding-bottom: 0;
                }

                #footerContent {
                    float: left;
                    width: 836px;
                }

                #footerSidebar {
                    margin: 0 0 0 864px;
                    width: 252px;
                }

                #header {
                    height: 130px;
                    padding: 32px;
                    position: relative;
                }

                #logo {
                    height: 130px;
                    left: 32px;
                    line-height: 130px;
                    position: absolute;
                    top: 32px;
                }

                #logo a {
                    color: #ffffff;
                    text-decoration: none;
                    text-shadow: 0 2px 2px #000000;
                }

                #logo h1 {
                    font-family: 'Yanone Kaffeesatz', sans-serif;
                    font-size: 3em;
                }

                #main {
                    background: #262626;
                    border-bottom: solid 1px #151515;
                    border-top: solid 1px #606060;
                    padding: 64px 32px 24px 32px;
                    position: relative;
                    text-shadow: 0 1px 0 #101010;
                    width: 1116px;
                }

                #main ul {
                    list-style: none;
                }

                #main ul li {
                    border-bottom: solid 1px #181818;
                    border-top: solid 1px #404040;
                    padding: 12px 0 12px 0;
                }

                #main ul li.first {
                    border-top: 0;
                    padding-top: 0;
                }

                #main ul li.last {
                    border-bottom: 0;
                    padding-bottom: 0;
                }

                #main ul.imageList {
                    list-style: none;
                }

                #main ul.imageList li {
                    padding: 20px 0 20px 0;
                }

                #main ul.imageList li.first {
                    padding-top: 0;
                }

                #main ul.imageList li.last {
                    padding-bottom: 0;
                }

                #main ul.imageList li img {
                    float: left;
                }

                #main ul.imageList li p {
                    margin: 0;
                    padding: 0;
                }

                #nav {
                    background: #6f2f2f;
                    border-top: solid 1px #ab6f6f;
                    font-family: 'Yanone Kaffeesatz', sans-serif;
                    font-size: 1.4em;
                    height: 50px;
                    line-height: 50px;
                    padding: 0 1em 0 1em;
                    position: absolute;
                    right: 32px;
                    top: 75px;
                }

                #nav a {
                    color: #ffffff;
                    text-decoration: none;
                    text-shadow: 0 2px 1px #3F1C1C;
                }

                #nav li {
                    margin: 0 1em 0 1em;
                }

                #nav ul {
                    list-style: none;
                }

                #nav ul li {
                    float: left;
                }

                #outer {
                    margin: 0 auto 0 auto;
                    position: relative;
                    width: 1180px;
                }

                #search input.button {
                    background: #6f2f2f;
                    border: 0;
                    color: #ffffff;
                    margin-left: 1em;
                    padding: 9px;
                }

                #search input.text {
                    border: solid 1px #ffffff;
                    padding: 8px;
                }

                #sidebar1 {
                    float: left;
                    padding: 0;
                    width: 252px;
                }

                #sidebar2 {
                    float: right;
                    padding: 0;
                    width: 252px;
                }
            </style>

        </head>

        <body>
            <div id="bg">
                <div id="outer">
                    <div id="header">
                        <div id="logo">
                            <h1>Recording for lab1</h1>
                        </div>
                    </div>
                    <div id="main">
                        <div id="sidebar1">
                            <h3>Students</h3>
                            <ul class="linkedList">
                                <li class="first"></li>
                                <li class="last"><a href="#student4">student4</a></li>
                            </ul>
                        </div>
                        <div id="content">
                            <div id="box1">
                                <h1 id="student4">lab1 - student4</h1>
                                <p><b>First submission for lab1: 4/14/2020 16:04:05</b></p>

                                <h2><code>test_file.txt</code> (a modification time)</h2>

                                <pre><code>
        some file contents
        and another line
                                </code></pre>

                                <p><b>no warnings: <code>a command</code></b></p>

                                <p><b>warnings: <code>another command</code></b></p>
                                <pre><code>
        output text
                                </code></pre>


                                <p><b>results of <code>a test command</code></b> (status: SUCCESS)</p>

                                <p><b>results of <code>other test command</code></b> (status: FILE_NOT_FOUND)</p>
                                <pre><code>
        more output
        another line
                                </code></pre>



                                <h2><code>another_file.txt</code></h2>

                                <p>File not found. <code>ls .</code> says that these files exist:</p>
                                <pre><code>
        a_third_file.txt
        more_files.txt
                                </code></pre>



                                <h2><code>optional.txt</code> (<b>optional submission</b>)</h2>

                                <p>File not found. <code>ls .</code> says that these files exist:</p>
                                <pre><code>
        yet_another_file.txt
                                </code></pre>



                                <h2><code>truncated.txt</code> (a modification time)</h2>

                                <pre><code>
        some tex
                                </code></pre>
                                <p><i>(truncated after 8 chars)</i></p>





                                <hr>

                            </div>
                        </div>
                        <br class="clear" />
                    </div>
                </div>
                <div id="copyright">
                    Created by StoGrade | Design: <a href="http://templated.org/free-css-templates/namelessgeometry/">
                    Nameless Geometry</a> by <a href="http://nodethirtythree.com">nodethirtythree</a> + <a
                        href="http://templated.org/">Templated.org</a>
                </div>
            </div>
        </body>

        </html>
        ''')


# ----------------------------- format_assignment_html -----------------------------

def test_format_assignment_html():
    formatted = format_assignment_html(RecordResult(spec_id='lab1',
                                                    student='student4',
                                                    first_submission='4/14/2020 16:04:05',
                                                    warnings=SubmissionWarnings(),
                                                    file_results=file_results))

    assert formatted.assignment == 'lab1'
    assert formatted.student == 'student4'
    assert formatted.type is FormatType.HTML
    assert '\n' + formatted.content == textwrap.dedent('''
        <h1 id="student4">lab1 - student4</h1>
        <p><b>First submission for lab1: 4/14/2020 16:04:05</b></p>

        <h2><code>test_file.txt</code> (a modification time)</h2>

        <pre><code>
        some file contents
        and another line
        </code></pre>

        <p><b>no warnings: <code>a command</code></b></p>

        <p><b>warnings: <code>another command</code></b></p>
        <pre><code>
        output text
        </code></pre>


        <p><b>results of <code>a test command</code></b> (status: SUCCESS)</p>

        <p><b>results of <code>other test command</code></b> (status: FILE_NOT_FOUND)</p>
        <pre><code>
        more output
        another line
        </code></pre>



        <h2><code>another_file.txt</code></h2>

        <p>File not found. <code>ls .</code> says that these files exist:</p>
        <pre><code>
        a_third_file.txt
        more_files.txt
        </code></pre>



        <h2><code>optional.txt</code> (<b>optional submission</b>)</h2>

        <p>File not found. <code>ls .</code> says that these files exist:</p>
        <pre><code>
        yet_another_file.txt
        </code></pre>



        <h2><code>truncated.txt</code> (a modification time)</h2>

        <pre><code>
        some tex
        </code></pre>
        <p><i>(truncated after 8 chars)</i></p>





        <hr>
        ''')


def test_format_assignment_html_error():
    # noinspection PyTypeChecker
    formatted = format_assignment_html(RecordResult(spec_id='hw1', student='student5',
                                                    file_results=5))

    assert formatted.assignment == 'hw1'
    assert formatted.student == 'student5'
    assert formatted.type is FormatType.HTML
    assert re.compile(r"^<pre><code>\nTraceback \(most recent call last\):"
                      r"[\s\S]*"
                      r"TypeError: &#x27;int&#x27; object is not iterable\n\n</code></pre>$").match(formatted.content)


@mock.patch('stograde.toolkit.global_vars.DEBUG', True)
def test_format_assignment_markdown_error_debug():
    try:
        # noinspection PyTypeChecker
        format_assignment_html(RecordResult(spec_id='hw1', student='student5',
                                            file_results=5))
        raise AssertionError
    except TypeError:
        pass


# ----------------------------- format_files_list -----------------------------

def test_format_files_list():
    formatted = format_files_list(file_results)

    assert '\n' + formatted == textwrap.dedent('''
        <h2><code>test_file.txt</code> (a modification time)</h2>

        <pre><code>
        some file contents
        and another line
        </code></pre>

        <p><b>no warnings: <code>a command</code></b></p>

        <p><b>warnings: <code>another command</code></b></p>
        <pre><code>
        output text
        </code></pre>


        <p><b>results of <code>a test command</code></b> (status: SUCCESS)</p>

        <p><b>results of <code>other test command</code></b> (status: FILE_NOT_FOUND)</p>
        <pre><code>
        more output
        another line
        </code></pre>



        <h2><code>another_file.txt</code></h2>

        <p>File not found. <code>ls .</code> says that these files exist:</p>
        <pre><code>
        a_third_file.txt
        more_files.txt
        </code></pre>



        <h2><code>optional.txt</code> (<b>optional submission</b>)</h2>

        <p>File not found. <code>ls .</code> says that these files exist:</p>
        <pre><code>
        yet_another_file.txt
        </code></pre>



        <h2><code>truncated.txt</code> (a modification time)</h2>

        <pre><code>
        some tex
        </code></pre>
        <p><i>(truncated after 8 chars)</i></p>




        ''')


# ----------------------------- format_header -----------------------------

def test_format_header_no_warnings():
    formatted = format_header(RecordResult('hw1', 'student1', '4/14/2020 13:22:45'), '')

    assert '\n' + formatted == textwrap.dedent('''
        <h1 id="student1">hw1 - student1</h1>
        <p><b>First submission for hw1: 4/14/2020 13:22:45</b></p>

        ''')


def test_format_header_with_warnings():
    formatted = format_header(RecordResult('hw1', 'student2'), '<p><b>a warning</b></p>')

    assert '\n' + formatted == textwrap.dedent('''
        <h1 id="student2">hw1 - student2</h1>
        <p><b>First submission for hw1: ERROR</b></p>
        <p><b>a warning</b></p>

        ''')


def test_format_header_assignment_missing():
    formatted = format_header(RecordResult('hw1', 'student1', '4/14/2020 13:22:45',
                                           SubmissionWarnings(assignment_missing=True)), '')

    assert '\n' + formatted == textwrap.dedent('''
        <h1 id="student1">hw1 - student1</h1>

        ''')


# ----------------------------- format_warnings -----------------------------

def test_format_warnings_none():
    assert format_warnings(SubmissionWarnings()) == ''


def test_format_warnings_missing():
    assert format_warnings(SubmissionWarnings(assignment_missing=True)) == '<p><b>No submission found</b></p>\n'


def test_format_warnings_unmerged_branches():
    formatted = format_warnings(SubmissionWarnings(unmerged_branches=['a branch', 'another branch']))

    assert '\n' + formatted == textwrap.dedent('''
        <p><b>Repository has unmerged branches:</b></p>
        <ul>
        <li>a branch</li>
        <li>another branch</li>
        </ul>''')


def test_format_warnings_record_error():
    assert format_warnings(
        SubmissionWarnings(recording_err='an error occurred')
    ) == '<p><b>Warning: an error occurred</b></p>'


# ----------------------------- format_file -----------------------------

def test_format_file():
    formatted = format_file(file_results[0])

    assert '\n' + formatted == textwrap.dedent('''
        <h2><code>test_file.txt</code> (a modification time)</h2>

        <pre><code>
        some file contents
        and another line
        </code></pre>

        <p><b>no warnings: <code>a command</code></b></p>

        <p><b>warnings: <code>another command</code></b></p>
        <pre><code>
        output text
        </code></pre>


        <p><b>results of <code>a test command</code></b> (status: SUCCESS)</p>

        <p><b>results of <code>other test command</code></b> (status: FILE_NOT_FOUND)</p>
        <pre><code>
        more output
        another line
        </code></pre>

        ''')


def test_format_file_missing():
    formatted = format_file(file_results[1])

    assert '\n' + formatted == textwrap.dedent('''
        <h2><code>another_file.txt</code></h2>

        <p>File not found. <code>ls .</code> says that these files exist:</p>
        <pre><code>
        a_third_file.txt
        more_files.txt
        </code></pre>

        ''')


def test_format_file_optional():
    formatted = format_file(file_results[2])

    assert '\n' + formatted == textwrap.dedent('''
        <h2><code>optional.txt</code> (<b>optional submission</b>)</h2>

        <p>File not found. <code>ls .</code> says that these files exist:</p>
        <pre><code>
        yet_another_file.txt
        </code></pre>

        ''')


# ----------------------------- format_file_contents -----------------------------

def test_format_file_contents_empty():
    assert format_file_contents(FileResult(file_name='a', contents='')) == '<p><i>File empty</i></p>'
    assert format_file_contents(FileResult(file_name='b', contents='   \n\t\n  ')) == '<p><i>File empty</i></p>'


def test_format_file_contents_with_contents():
    simple_contents = textwrap.dedent('''
        int main() {
            return 0;
        }''')

    formatted = '\n' + format_file_contents(FileResult(file_name='',
                                                       contents=simple_contents))

    assert formatted == textwrap.dedent('''
        <pre><code>

        int main() {
            return 0;
        }
        </code></pre>''')


# ----------------------------- format_file_compilation -----------------------------

def test_format_file_compilation_no_warnings():
    formatted = format_file_compilation([compile_results[0]])
    assert formatted == '<p><b>no warnings: <code>test command</code></b></p>\n'


def test_format_file_compilation_warnings():
    formatted = format_file_compilation([compile_results[1]])
    assert '\n' + formatted == textwrap.dedent('''
        <p><b>warnings: <code>test command 2</code></b></p>
        <pre><code>
        some output
        </code></pre>
        ''')


def test_format_file_compilation_multiple_commands():
    formatted = format_file_compilation(compile_results)
    assert '\n' + formatted == textwrap.dedent('''
        <p><b>no warnings: <code>test command</code></b></p>

        <p><b>warnings: <code>test command 2</code></b></p>
        <pre><code>
        some output
        </code></pre>

        <p><b>warnings: <code>test command 3</code></b></p>
        <pre><code>
        more
        </code></pre>

        <p><i>(truncated after 4 chars)</i></p>
        ''')


# ----------------------------- format_file_tests -----------------------------

def test_format_file_tests_no_output():
    formatted = format_file_tests([test_results[0]])
    assert '\n' + formatted == textwrap.dedent('''
        <p><b>results of <code>test command</code></b> (status: SUCCESS)</p>
        ''')


def test_format_file_tests_output():
    formatted = format_file_tests([test_results[1]])
    assert '\n' + formatted == textwrap.dedent('''
        <p><b>results of <code>other command</code></b> (status: SUCCESS)</p>
        <pre><code>
        some more output
        and another line
        </code></pre>
        ''')


def test_format_file_tests_truncated_output():
    formatted = format_file_tests([test_results[2]])
    assert '\n' + formatted == textwrap.dedent('''
        <p><b>results of <code>a third command</code></b> (status: SUCCESS)</p>
        <pre><code>
        more
        </code></pre>
        <p><i>(truncated after 4 chars)</i></p>
        ''')


def test_format_file_tests_multiple_commands():
    formatted = format_file_tests(test_results)
    assert '\n' + formatted == textwrap.dedent('''
        <p><b>results of <code>test command</code></b> (status: SUCCESS)</p>

        <p><b>results of <code>other command</code></b> (status: SUCCESS)</p>
        <pre><code>
        some more output
        and another line
        </code></pre>

        <p><b>results of <code>a third command</code></b> (status: SUCCESS)</p>
        <pre><code>
        more
        </code></pre>
        <p><i>(truncated after 4 chars)</i></p>
        ''')


# ----------------------------- format_as_code -----------------------------

def test_format_as_code():
    assert format_as_code('some code') == '<pre><code>\nsome code\n</code></pre>'
    assert format_as_code('') == ''


# ----------------------------- format_as_ul -----------------------------

def test_format_as_ul():
    assert format_as_ul(['list item']) == '<ul>\n<li>list item</li>\n</ul>'
    assert format_as_ul(['list item', 'list item 2']) == '<ul>\n<li>list item</li>\n<li>list item 2</li>\n</ul>'
    assert format_as_ul([]) == ''
