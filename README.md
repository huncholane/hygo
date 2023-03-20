# Set up for Development

Run the init script
`./init.sh`

- Copies the env templates into a .env file if you don't already have one.
- Starts a virtual environment and appends `source dev.sh` to it
- Installs requirements for python and packages for frontend

## Now, you need to fill in the env variables

- [SPOTIFY_CLIENT_ID](#spotify-settings)
- [SPOTIFY_CLIENT_SECRET](#spotify-settings)
- [DJANGO_SECRET_KEY](#spotify-settings)
- [SPOTIFY_REDIRECT_URI](#spotify-settings)
- [NGINX_PORT](#ssh-tunneling)
- [TUNNEL_HOST](#ssh-tunneling)
- [TUNNEL_PORT](#ssh-tunneling)

# Spotify Settings

To get the spotify client id and secrets you need to create them here https://developer.spotify.com/dashboard/applications

![Spotify App Settings](https://cdn.discordapp.com/attachments/985857396641529876/1087357575667925082/image.png)

# SSH Tunneling

### You need a server you have access to that faces the world

- These values link [spotify](#spotify-settings) to the server running on your localhost
- NGINX_PORT will be the port used by the default.conf inside of the nginx folder with the dev-compose
  - This port combines backend 8000 and frontend 5173 into one port
  - This allows us to forward backend requests for /admin/ and /api/
- TUNNEL_HOST is the configuration you use to ssh into your server so include user and credentials in this string. i.e. `ssh TUNNEL_HOST`
- TUNNEL_PORT this is the port that your local host will be tied to on the server

# Bringing it all together

The dev.sh file has some handy functions

- dev: Start the ssh tunnel, dev-compose, frontend, and backend on the localhost
  - Doing it this way allows for instant updates to the frontend and backend servers
- gcom: `git add . && git commit -m your commit message without any quotes`
  - I just love this shortcut
