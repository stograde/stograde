# StoGrade Referee

StoGrade Referee is a tool that, for all intensive purposes, has been superseded by `stograde ci`.
Its codebase has not been updated in many years.
But, because the code still exists, here is the documentation that was created for it:

## Referee Documentation from CarlHacks 2017

- Make a VM (ping cluster managers)
- Install docker
- Install apache2
- Enable cgi-bin
- Add $IP (192.168.0.26)/cgi-bin/referee.sh as a PUSH webhook on a repository on Stogit
- Add the ssh key from the VM to an account on Stogit

### cron
There are somewhere around 3 crontabs.

1. (daily) Update Docker image locally on machine. Since this is a transitory process and isn’t always running, there is
no downtime, per se, but requests made during a tiny interval will fail. (This is run at midnight, which is a pretty safe
time.)
2. (daily) Git: Pull the toolkit. Since our scripts are run from the toolkit’s repository, we should keep this up-to-date
on the server. Only the master branch is pulled.
3. (daily) Git: Pull the specs. Since the specs can change over time, we should keep them up-to-date.

The contents of these are stored in [`/script/crontab`](https://github.com/StoDevX/stograde/blob/master/script/crontab).

## email
Referee sends email through Gmail’s smtp server, which means that we have to authenticate with gmail. Set the
`STOGRADE_EMAIL_USERNAME` and `STOGRADE_EMAIL_PASSWORD` environment variables by way of editing the file
`/home/referee/gmail_auth.sh` (which is a docker env file, not a shell script).

## env vars
- `STOGRADE_EMAIL_USERNAME`: the username to authenticate to gmail with
- `STOGRADE_EMAIL_PASSWORD`: the password to authenticate to gmail with


