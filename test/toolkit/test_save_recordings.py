import os
import textwrap
from unittest import mock

from stograde.common.run_status import RunStatus
from stograde.formatters.format_type import FormatType
from stograde.formatters.formatted_result import FormattedResult
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.process_file.compile_result import CompileResult
from stograde.process_file.file_result import FileResult
from stograde.process_file.test_result import TestResult
from stograde.student.student_result import StudentResult
from stograde.toolkit.save_recordings import record_recording_to_disk, save_recordings


def test_record_recording_to_disk(tmpdir):
    with tmpdir.as_cwd():
        record_recording_to_disk([FormattedResult(assignment='hw1',
                                                  content='some content',
                                                  student='z',
                                                  type=FormatType.MD),
                                  FormattedResult(assignment='hw1',
                                                  content='some more content',
                                                  student='a',
                                                  type=FormatType.MD),
                                  FormattedResult(assignment='hw1',
                                                  content='even more content',
                                                  student='b',
                                                  type=FormatType.MD)],
                                 file_identifier='hw1',
                                 format_type=FormatType.MD)

        assert os.path.exists(os.path.join('logs', 'log-hw1.md'))

        with open(os.path.join('logs', 'log-hw1.md')) as file:
            contents = file.read()
            file.close()

        assert contents == ('some more content\n'
                            'even more content\n'
                            'some content')


def test_record_recording_to_disk_error(capsys):
    with mock.patch('os.makedirs', side_effect=TypeError('An error was thrown')):
        record_recording_to_disk([], 'hw1', FormatType.MD)

    _, err = capsys.readouterr()

    assert err == 'Could not write recording for hw1: An error was thrown\n'


file_results = [FileResult(file_name='test_file.txt',
                           contents='some file contents\nand another line',
                           compile_results=[CompileResult('a command', '', RunStatus.SUCCESS),
                                            CompileResult('another command', 'output text', RunStatus.SUCCESS)],
                           test_results=[TestResult('a test command', '', error=False, status=RunStatus.SUCCESS),
                                         TestResult('other test command', 'more output\nanother line',
                                                    error=True, status=RunStatus.FILE_NOT_FOUND)],
                           last_modified='a modification time'),
                FileResult(file_name='another_file.txt',
                           file_missing=True,
                           other_files=['a_third_file.txt', 'more_files.txt']),
                FileResult(file_name='optional.txt',
                           file_missing=True,
                           other_files=['yet_another_file.txt'],
                           optional=True)]


def test_save_recordings_disk_md(tmpdir):
    with tmpdir.as_cwd():
        save_recordings([StudentResult(name='z',
                                       results=[RecordResult(spec_id='hw1',
                                                             student='student4',
                                                             first_submission='4/14/2020 16:04:05',
                                                             warnings=SubmissionWarnings(),
                                                             file_results=file_results)])],
                        '',
                        False,
                        FormatType.MD)

        assert os.path.exists(os.path.join('logs', 'log-hw1.md'))

        with open(os.path.join('logs', 'log-hw1.md')) as file:
            contents = file.read()
            file.close()

        assert '\n' + contents == textwrap.dedent('''
                # hw1 – student4
                First submission for hw1: 4/14/2020 16:04:05


                ## test_file.txt (a modification time)

                ```txt
                some file contents
                and another line
                ```

                **no warnings: `a command`**

                **warnings: `another command`**

                ```
                output text
                ```

                **results of `a test command`** (status: SUCCESS)

                **results of `other test command`** (status: FILE_NOT_FOUND)

                ```
                more output
                another line
                ```


                ## another_file.txt

                File not found. `ls .` says that these files exist:
                ```
                a_third_file.txt
                more_files.txt
                ```


                ## optional.txt (**optional submission**)

                File not found. `ls .` says that these files exist:
                ```
                yet_another_file.txt
                ```


                ''')


def test_save_recordings_disk_html(tmpdir):
    with tmpdir.as_cwd():
        save_recordings([StudentResult(name='z',
                                       results=[RecordResult(spec_id='hw1',
                                                             student='student4',
                                                             first_submission='4/14/2020 16:04:05',
                                                             warnings=SubmissionWarnings(),
                                                             file_results=file_results)])],
                        '',
                        False,
                        FormatType.HTML)

        assert os.path.exists(os.path.join('logs', 'log-hw1.html'))

        with open(os.path.join('logs', 'log-hw1.html')) as file:
            contents = file.read()
            file.close()

        assert '\n' + contents == textwrap.dedent('''

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
                    <title>hw1</title>
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
                                    <h1>Recording for hw1</h1>
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
                                        <h1 id="student4">hw1 - student4</h1>
                                        <p><b>First submission for hw1: 4/14/2020 16:04:05</b></p>

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


def test_save_recording_gist(capsys):
    with mock.patch('stograde.toolkit.save_recordings.post_gist') as mock_gist:
        mock_gist.return_value = 'a_url'
        save_recordings([StudentResult(name='z',
                                       results=[RecordResult(spec_id='hw1',
                                                             student='student4',
                                                             first_submission='4/14/2020 16:04:05',
                                                             warnings=SubmissionWarnings(),
                                                             file_results=file_results)])],
                        'the table',
                        True)

        assert mock_gist.call_args[0][0] == 'log for hw1'
        assert mock_gist.call_args[0][1] == {'-stograde report hw1 table.txt': {'content': 'the table'},
                                             'student4.md':
                                                 {'content': '# hw1 – student4\n'
                                                             'First submission for hw1: 4/14/2020 16:04:05\n\n\n'
                                                             '## test_file.txt (a modification time)\n\n'
                                                             '```txt\n'
                                                             'some file contents\n'
                                                             'and another line\n'
                                                             '```\n\n'
                                                             '**no warnings: `a command`**\n\n'
                                                             '**warnings: `another command`**\n\n'
                                                             '```\n'
                                                             'output text\n'
                                                             '```\n\n'
                                                             '**results of `a test command`** (status: SUCCESS)\n\n'
                                                             '**results of `other test command`** '
                                                             '(status: FILE_NOT_FOUND)\n\n'
                                                             '```\n'
                                                             'more output\n'
                                                             'another line\n'
                                                             '```\n\n\n'
                                                             '## another_file.txt\n\n'
                                                             'File not found. `ls .` says that these files exist:\n'
                                                             '```\n'
                                                             'a_third_file.txt\n'
                                                             'more_files.txt\n'
                                                             '```\n\n\n'
                                                             '## optional.txt (**optional submission**)\n\n'
                                                             'File not found. `ls .` says that these files exist:\n'
                                                             '```\n'
                                                             'yet_another_file.txt\n'
                                                             '```'}}

    out, _ = capsys.readouterr()

    assert out == 'hw1 results are available at a_url\n'


def test_save_recording_bad_formatter():
    try:
        # noinspection PyTypeChecker
        save_recordings([], '', False, 5)
        raise AssertionError
    except ValueError:
        pass
