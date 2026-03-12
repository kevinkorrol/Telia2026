FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

# Run the app when the container launches
CMD ["npm", "run", "dev", "--", "--host"]
