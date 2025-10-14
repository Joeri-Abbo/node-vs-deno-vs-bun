FROM oven/bun:1.0.7

WORKDIR /app

# Copy package files
COPY package.json bun.lockb* ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN bun run build

# Expose port
EXPOSE 3003

# Set environment variable
ENV PORT=3003

# Start the application
CMD ["bun", "start"]