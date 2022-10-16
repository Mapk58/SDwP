# installation
1. Install docker into your system
2. clone repo into suitable folder
3. Edit `Dockerfile`, where change `ENV BOT_TOKEN = X` for your bot token
2. run `docker build ./ -t gangof6/sdwp:0.0.1`
3. run `docker run -d --restart=always gangof6/sdwp:0.0.1`