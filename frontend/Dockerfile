FROM node:16

WORKDIR /app

# Copy package files and install dependencies.
COPY package*.json ./
RUN npm install

# Copy the rest of the source code.
COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve"]
