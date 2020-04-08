# Grading React App Files with `stograde web`

Files created for the SD React App need to be graded differently.
They need the browser React app to view how they render.
This poses an issue, as the toolkit was originally designed for homeworks that only use the command line.
A command line interface was designed that allows you to view students' files in the app.

### Starting the CLI

The CLI requires three flags:
- `--record HW` - telling the toolkit which homework to grade for
- `--web` - indicating that you want to use the web CLI
- `--port PORT` - setting the port that the server uses to communicate with the app.
This port is different for each React app user, so you can figure it out by opening the app and looking at the network logs.
The IP it is connecting to will be listed, along with a `:` and a number.
That last number is your port.  

A web server like the `~/bridge.py` used by students is started in a separate thread.
Then a command line interface is started that allows you to choose what file to render.

### Using the CLI

The interface starts by updating all student repos.
It will say `Loading repos. Please wait...`.
When this is done, it will show a list of students to choose from:

```
? Choose student  (Use arrow keys)
   QUIT
   rives
   student1
   magnusow
   volz
   piersonv
   narvae1
``` 

Select a student using the arrow keys and enter.
This will show a `Processing...` message, then show you a list of all files in the homework.

```
? Choose student  narvae1
Processing...
? Choose file  (Use arrow keys)
   BACK
   story.cpp
   weather.cpp
   weather2.cpp
```

Select the file using the arrow keys and enter.
This will compile it and redirect the server to deliver the new executable when the client asks.
