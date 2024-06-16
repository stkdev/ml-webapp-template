FROM node:20

WORKDIR /app

COPY package.json package-lock.json ./
COPY *.js ./

RUN npm ci
COPY . .
RUN npm run build
RUN npm rebuild esbuild

CMD ["npm", "run", "dev", "--", "--host"]
