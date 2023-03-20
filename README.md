# Set up for Development

Run the init script `./init.sh` or `bash init.sh`

- Copies the env templates into a .env file if you don't already have one.
- Starts a virtual environment and appends `source dev.sh` to it
- Installs requirements for python and packages for frontend
  Next you need to activate the venv
- `source venv/**/activate`

## Now, you need to fill in the env variables

- [DJANGO_SECRET_KEY](#django-secret)
- [SPOTIFY_CLIENT_ID](#spotify-settings)
- [SPOTIFY_CLIENT_SECRET](#spotify-settings)
- [SPOTIFY_REDIRECT_URI](#spotify-settings)
- [NGINX_PORT](#ssh-tunneling)
- [TUNNEL_HOST](#ssh-tunneling)
- [TUNNEL_PORT](#ssh-tunneling)

# Django Secret

- Type djsecret and you get a new secret
- Copy this into your .env

# Spotify Settings

## [Spotify Application](https://developer.spotify.com/dashboard/applications)

- Create an application [here](https://developer.spotify.com/dashboard/applications)
- SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
  ![SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET](https://cdn.discordapp.com/attachments/985857396641529876/1087365234290864148/image.png)

## Use the [SSH Tunnel](#ssh-tunneling) inside of these settings

![Spotify App Settings](https://cdn.discordapp.com/attachments/985857396641529876/1087357575667925082/image.png)

# SSH Tunneling

### You need a server you have access to that faces the world

- These values link [spotify](#spotify-settings) to the server running on your localhost
- NGINX_PORT will be the port used by the default.conf inside of the nginx folder with the dev-compose
  - This port combines backend 8000 and frontend 5173 into one port
  - This allows us to forward backend requests for /admin/ and /api/ and frontend requests to all other endpoints
- TUNNEL_HOST is the configuration you use to ssh into your server so include user and credentials in this string. i.e. `ssh TUNNEL_HOST`
- TUNNEL_PORT this is the port that your local host will be tied to on the server

# Bringing it all together

The dev.sh file has some handy functions

- `dev`: Start the ssh tunnel, dev-compose, frontend, and backend on the localhost
  - Doing it this way allows for instant updates to the frontend and backend servers
- `gcom`: `git add . && git commit -m your commit message without any quotes`
- `vsource`: `source venv/**/activate`
  - Reloads the source
- `dj`: `python manage.py $@`
  - Finds the manage.py file and runs the rest of the argumanets
- `djs`: Shortcut to start the backend server
- `djsecret`: Creates a new django secret key

![Cool AI Picture](https://cdn.discordapp.com/attachments/1071695170610925638/1076982838148223137/huncholane_ghost_hacker_21d6f9b3-a6b6-45fe-939d-9d6769a4e672.png)
