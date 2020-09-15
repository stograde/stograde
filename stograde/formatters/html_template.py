import textwrap
from typing import List

html_style = '''<style>
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
'''

html_template = '''
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
    <title>{assignment}</title>
    <link href="http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz" rel="stylesheet" type="text/css" />
    {style}
</head>

<body>
    <div id="bg">
        <div id="outer">
            <div id="header">
                <div id="logo">
                    <h1>Recording for {assignment}</h1>
                </div>
            </div>
            <div id="main">
                <div id="sidebar1">
                    <h3>Students</h3>
                    <ul class="linkedList">
{student_list}
                    </ul>
                </div>
                <div id="content">
                    <div id="box1">
{content}
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
'''


def add_styling(assignment: str, students: List[str], content: str) -> str:
    student_links = ['<a href="#{student}">{student}</a>'.format(student=student) for student in students]
    student_list = ''.join(['<li class="first">',
                            '</li>\n<li>'.join(student_links[:-1]),
                            '</li>\n',
                            '<li class="last">',
                            student_links[-1],
                            '</li>'])

    return html_template.format(style=html_style,
                                assignment=assignment,
                                student_list=textwrap.indent(student_list, ' ' * 24),
                                content=textwrap.indent(content,
                                                        ' ' * 24,
                                                        lambda line: line[0] == '<'))
