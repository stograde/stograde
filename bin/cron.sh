#!/bin/bash

git add .
git stash
git pull --rebase

{
	boundary='BLAH.BLAH/hawken.mackay.riv.es'
	subject='Daily CS251 Homework Submission Update'
	echo From: rives@stolaf.edu
	echo To: rives@stolaf.edu
	echo Subject: "$subject"
	echo MIME-Version: 1.0
	echo Content-Type: multipart/alternative;
	echo
	echo "$boundary"
	echo Content-Type: text/html

	TABLE=$(./update.py -w8 --all --no-progress)

	echo "<html>"
	echo "<head>"
	echo "<title>$subject</title>"
	echo "</head>"
	echo "<body>"
	echo "<pre>"
	echo "$TABLE"
	echo "</pre>"
	echo "</body>"
	echo "</html>"
	echo "--all--$boundary"
} | sendmail -t
