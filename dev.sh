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
# IS_DOCKER
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
    local start=$(pwd)
    get_to_root

    docker compose down --remove-orphans
    docker compose -f dev-compose.yml up -d

    cd frontend && npm run dev &
    cd backend && python manage.py runserver
}

function gcom () {
    local message=$@
    oecho "$message"
    git add . && git commit -m "$message"
}

function vsource () {
    start=$(pwd)
    get_to_root
    source venv/**/activate
    cd $start
}

function dj () {
    start=$(pwd)
    get_to_root
    cd backend
    python manage.py $@
    cd $start
}

function djsecret() {
    dj createsecret
}

function preq () {
    local start=$(pwd)
    get_to_root
    cd backend
    pip install -r requirements.txt
    cd $start
}

function tunnel () {
    ssh -R $1:localhost:$2 $3 -N
}
