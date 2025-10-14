FROM denoland/deno:latest

WORKDIR /app

# Copy Deno configuration files
COPY deno.json ./
COPY package.json ./

# Copy source code
COPY . .


# Build the application using Deno
# Install Node.js (needed because Next's install step spawns `npm`)
RUN apt-get update \
	&& apt-get install -y curl ca-certificates gnupg build-essential \
	&& curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
	&& apt-get install -y nodejs \
	&& npm --version \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install npm dependencies so Next won't try to spawn npm at build-time
RUN npm install --legacy-peer-deps

# Ensure TypeScript (and node types) are present so Next doesn't try to
# install them during build when it detects TS files.
RUN npm install --no-audit --no-fund --save-dev typescript @types/node@^18

# Optional: install sharp via deno's npm compatibility if needed
RUN deno install --allow-scripts=npm:sharp

# Run build via Deno task
RUN deno task build

# Expose port
EXPOSE 3002

# Set environment variable
ENV PORT=3002

# Start the application using Deno
CMD ["deno", "task", "start"]