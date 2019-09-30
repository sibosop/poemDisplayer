# poemDisplayer
Read the Raspmus project Readme for a full setup
* `crontab -e`
* Note: use -c with relative path (speclib/<json file) if it's not raspmus.json
* `MAILTO=""`
* `@reboot sleep 20; /home/pi/GitProjects/poemDisplayer/poemDisplayerWrap.sh -c speclib/poem.json 2>&1 | logger -t poem`
