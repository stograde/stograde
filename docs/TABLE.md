# Getting an Overview of Submissions with `stograde table`

A chart can be printed out to give you an overview of what has been turned in.
(This only checks if the file has been submitted.
It does *not* check if the file compiles properly or if its tests pass.)

Running `stograde table` will produce something like this:

```
USER       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 5 6 7 8 9 10 11 | 1 2
–––––––––––+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+––––––––––––––––––––––––-|-----
rives      | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11 | 1 - 
student1   | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– –– –– 17 18 19 –– –– –– –– –– –– | 1 2 – 4 – 6 7 – – –– –– | - - 
magnusow   | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – – 7 8 9 10 11 | 1 2 
volz       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11 | 1 2 
piersonv   | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11 | - 2
```

The first set of columns are the homeworks, the second are the labs, and the third are the worksheets.

### Options

You can use the `--section` and `--students` arguments to filter which students are processed.

- `--section` relies on there being sections in the `students.txt` file
- `--students` overrides all of the other options.
For example, `--students rives piersonv` would only look at those two students.

You can use the `--sort-by` argument to sort the table, as well.
`name` is the default, sorting by username.
`count` sorts by the number of completed submissions.

If you want the table as quickly as possible, pass `-R`/`--skip-repo-check` to bypass the remote repository check.

`--no-partials` can be passed to disable highlighting of any partial submissions.

For other options, run `stograde table -h`.
