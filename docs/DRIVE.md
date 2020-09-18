# Checking Google Drive Submissions with `stograde drive`

`stograde drive` is used to determine who has shared a Google Doc with the TAs for grading, and collects the links for all of those documents in one place.

## Setting Up an OAuth 2.0 Client ID

`stograde drive` needs to be able to communicate with the Google Drive API.
Because sharing an API key publicly is a bad idea, you will need to create your own.
Creating a key is free and is done through the Google Cloud Platform.

### Creating a Project

Navigate to [https://console.developers.google.com](https://console.developers.google.com).
Make sure you are signed in with your school account (account select is in the top right corner).

If you haven't used the Google Cloud Platform before, you may see a popup like this.
Check the box and click `AGREE AND CONTINUE`.

![Step 0](images/StoGrade_drive_key_step0.png)

You will then see a screen like this.
Click `CREATE PROJECT` on the right.

![Step 1](images/StoGrade_drive_key_step1.png)

Name the project `StoGrade`, and set the organization and location to `stolaf.edu`.
(If `stolaf.edu` doesn't show up, make sure you're using your school account).

![Step 2](images/StoGrade_drive_key_step2.png)

After a minute, the bell in the top right corner will indicate you have a notification.
Click on the bell and click `SELECT PROJECT` for the `Create Project: StoGrade` notification.

![Step 3](images/StoGrade_drive_key_step3.png)

### Enabling the Google Drive API

Click on `ENABLE APIS AND SERVICES` at the top of the screen.

![Step 4](images/StoGrade_drive_key_step4.png)

Type `drive` into the search bar and click on `Google Drive API`.

![Step 5](images/StoGrade_drive_key_step5.png)

Click `ENABLE`.

![Step 6](images/StoGrade_drive_key_step6.png)

You should now see a screen like this.

### Configuring the App's Consent Screen

![Step 7](images/StoGrade_drive_key_step7.png)

Open the main side menu (hamburger icon in the top left), hover over `APIs & Services` and click `Credentials`.

![Step 8](images/StoGrade_drive_key_step8.png)

Click on `CONFIGURE CONSENT SCREEN` in the top right.

![Step 9](images/StoGrade_drive_key_step9.png)

Select `Internal` as the user type.
This limits the usage of the key to the `stolaf.edu` domain.
It also means we won't get a message each time we use it warning us about the security of our app.

![Step 10](images/StoGrade_drive_key_step10.png)

Enter `StoGrade` for the application name.
Scroll down and click `Save`.   

![Step 11](images/StoGrade_drive_key_step11.png)

### Creating Our Credentials

You should see a screen like this.
Click on `Credentials` in the menu on the left.

![Step 12](images/StoGrade_drive_key_step12.png)

Click on `CREATE CREDENTIALS` at the top of the screen and select `OAuth client ID`.

![Step 13](images/StoGrade_drive_key_step13.png)

Select `Desktop app` as the Application type and name it `StoGrade Client`.
Click `CREATE`.

![Step 14](images/StoGrade_drive_key_step14.png)

There will be a popup with the credentials that you just created.
Click `OK`.

![Step 15](images/StoGrade_drive_key_step15.png)

### Downloading Our Credentials

Click on the OAuth 2.0 Client ID you just created.

![Step 16](images/StoGrade_drive_key_step16.png)

Click `DOWNLOAD JSON` at the top.

![Step 17](images/StoGrade_drive_key_step17.png)

This will download a JSON representation of your secret key.

Rename the file to `client_secret.json` and copy it to the directory where your `students.txt` is located.


## Running `stograde drive`

`stograde drive` requires a positional argument for the assignment to grade, as well as the `--email` (or `-e`) flag.
This flag indicates the group email (e.g. `hd-tas` or `hd-tas@stolaf.edu`) that the student's have been sharing their documents with and is used to filter out files not shared with that group email.

e.g. `stograde drive hw1 --email hd-tas`

The app will then prompt you to open a long link in your browser.

Open that link and select your `stolaf.edu` email account.

Click `Allow`.

![Drive Authentication](images/StoGrade_drive_auth.png)

You will then get a key to copy.
Paste this key into the prompt in your terminal.

![Drive Auth Key](images/StoGrade_drive_auth_key.png)
