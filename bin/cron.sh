#!/bin/bash

git add .
git stash
git pull --rebase

{
	echo To: rives@stolaf.edu, allen@stolaf.edu
	echo Subject: Daily CS251 Homework Submission Update
	echo From: rives@stolaf.edu

	./update.py -w8 --all --no-progress
} | sendmail -t
