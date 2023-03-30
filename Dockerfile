FROM huncho/web

# install node dependencies
COPY ./frontend/package.json /frontend/package.json
WORKDIR /frontend
RUN npm install

# install python dependencies
COPY ./backend/requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN pip install -r requirements.txt

WORKDIR /
COPY ./web.sh /web.sh
RUN chmod 777 /web.sh

CMD ["/web.sh"]