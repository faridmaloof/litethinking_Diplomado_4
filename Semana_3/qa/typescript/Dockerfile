FROM node:22-alpine

WORKDIR /qa-typescript

COPY package.json tsconfig.json ./
RUN npm install

COPY src ./src

CMD ["npm", "run", "validate"]
