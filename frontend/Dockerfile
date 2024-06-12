FROM node:18-alpine

WORKDIR /TochkaBookingProject

COPY frontend/ .

RUN npm install
RUN npm install serve -g

CMD ["serve", "-s", "dist"]

