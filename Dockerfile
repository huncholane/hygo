FROM huncho/web:latest

# install node dependencies
COPY ./frontend/package.json /frontend/package.json
WORKDIR /frontend
RUN npm install

# install python dependencies
COPY ./backend/requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN pip install -r requirements.txt

# configure node
COPY ./frontend /frontend
WORKDIR /frontend
# RUN npm run build

# configure django
COPY ./backend /backend
WORKDIR /backend

WORKDIR /
COPY ./web.sh /web.sh
RUN chmod 777 /web.sh

VOLUME ./test /backend
CMD ["/web.sh"]