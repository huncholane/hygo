#!/bin/bash
# Source this script to the venv and you can type dev to run the server

# load the .env variables
# NGINX_PORT
# TUNNEL_HOST
# TUNNEL_PORT
# DJANGO_SECRET_KEY
# SPOTIFY_REDIRECT_URI
# SPOTIFY_CLIENT_ID
# SPOTIFY_CLIENT_SECRET
# IS_DOCKERR
set -a
source .env
set +a

function get_to_root () {
    for i in $(seq 1 5); do
        if test -f dev.sh; then
            break
        else
            cd ..
        fi
    done
}


function dev () {
    # tunnel the server
    local start=`pwd`
    for i in $(seq 1 5); do
        if test -f dev.sh; then
            break
        else
            cd ..
        fi
    done
    if ! test -f dev.sh; then
        echo "Could not find dev.sh"
        cd $start
        return
    fi
    ssh -R $TUNNEL_PORT:localhost:$NGINX_PORT $TUNNEL_HOST -N &

    docker compose -f dev-compose.yml up -d 2> /dev/null

    cd backend && python manage.py runserver &
    cd frontend && npm run dev
}

function gcom () {
    local message=$@
    oecho "$message"
    git add . && git commit -m "$message"
}

function vsource () {
    start=`pwd`
    get_to_root
    source venv/**/activate
    cd $start
}

function dj () {
    start=`pwd`
    get_to_root
    cd backend
    python manage.py $@
    cd $start
}

function djsecret() {
    dj createsecret
}