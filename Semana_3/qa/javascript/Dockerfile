FROM node:22-alpine

WORKDIR /qa-javascript

COPY package.json .
COPY scripts ./scripts

CMD ["npm", "run", "validate"]
