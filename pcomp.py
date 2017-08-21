import shlex
import subprocess
import argparse
import os
import difflib
import sys

html_begin ='''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>teffer</title>
  <style type="text/css">
    table.diff {font-family:Courier; border:medium;}
    .diff_header {background-color:#e0e0e0}
    td.diff_header {text-align:right}
    .diff_next {background-color:#c0c0c0}
    .diff_add {background-color:#aaffaa}
    .diff_chg {background-color:#ffff77}
    .diff_sub {background-color:#ffaaaa}
  </style>
</head>
<body>
'''
html_legend = '''
<table class="diff" summary="Legends">
  <tr> <th colspan="2"> Legends </th> </tr>
  <tr> <td> 
  <table border="" summary="Colors">
    <tr><th> Colors </th> </tr>
    <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
    <tr><td class="diff_chg">Changed</td> </tr>
    <tr><td class="diff_sub">Deleted</td> </tr>
  </table> </td> <td>
  <table border="" summary="Links">
    <tr><th colspan="2"> Links </th> </tr>
    <tr><td>(f)irst change</td> </tr>
    <tr><td>(n)ext change</td> </tr>
    <tr><td>(t)op</td> </tr>
  </table> </td> </tr>
</table>
'''
html_end = '''
</body>
</html>
'''

expected = "expected.txt"
actual   = "actual.txt"

help_str = '''
The argument to this script are all positional, other than the help command.
If the first argument is -h, this message will be printed.
Otherwise, the first argument is always assumed to be the diff output directory.
All following arguments are the files to diff against one-another.
'''

output = 'diff'
if not os.path.exists(output):
    os.makedirs(output)

file_counter = 0
index_file = open(os.path.join(output, 'index.html'), "w")
index_file.write(html_begin)
index_file.write('<h1>teffer diff results</h1>')
index_file.write('<hr>')

if(len(sys.argv) <= 2):
    print(help_str)
    sys.exit()

files = sys.argv[2:]

diff_map = {}

for i in files:
    for j in files:
        if i != j:
            i_lines = open(i, 'U').readlines()
            j_lines = open(j, 'U').readlines()
            diff = difflib.HtmlDiff().make_table(i_lines, j_lines, i, j)

            dfn = str(file_counter) + '.html'
            diff_file = open(os.path.join(output, dfn), "w")
            file_counter += 1
            
            diff_file.write(html_begin)
            diff_file.write('<h1>teffer diff results</h1>')
            diff_file.write('<h2>' + i + ' -- ' + j + '</h2>')
            diff_file.write('<br>')
            diff_file.write(diff)
            diff_file.write('<br>')
            diff_file.write(html_end)


            lines = max(len(i_lines), len(j_lines)) * 2

            difference = 0
            for line in difflib.unified_diff(i_lines, j_lines, fromfile=i, tofile=j):
                 if line.startswith('-') or line.startswith('+'):
                     difference += 1
            rating = difference / lines
            
            link = '<h2><a href="' + dfn + '">' + i + ' and ' + j + ' ( ' + str(round(rating, 2)) + ' difference) </h2>'
            
            diff_map[rating] = link

for key in sorted(diff_map.keys()):
    index_file.write('<br>')
    index_file.write(diff_map[key])
    index_file.write('<br>')
        
index_file.write('<br>')
index_file.write(html_end)
index_file.close()

