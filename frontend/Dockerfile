FROM node:22

WORKDIR /TochkaBookingProject

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .

CMD ["npm", "run", "dev"]
