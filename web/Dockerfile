# Stage 1: Build the Next.js app
FROM node:18-alpine AS builder

WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm

# Copy package files and install dependencies using pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --production=false

# Copy only the necessary source files (excluding unnecessary files)
COPY . .

# Build the Next.js app
RUN pnpm build

# Stage 2: Serve the Next.js app with a lightweight server
FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy only the static build output from Next.js (not the entire .next folder)
COPY --from=builder /app/.next/static /usr/share/nginx/html/static
COPY --from=builder /app/public /usr/share/nginx/html/public

# Copy the custom Nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["pnpm", "start"]
