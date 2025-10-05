FROM node:20-bookworm-slim

# Set working directory
WORKDIR /app

# Install dependencies first (leverage Docker layer caching)
COPY package.json package-lock.json* ./

# If a lockfile exists, use npm ci for reproducible installs. Fallback to npm install otherwise.
RUN if [ -f package-lock.json ]; then \
			npm ci --no-audit --no-fund; \
		else \
			npm install --no-audit --no-fund; \
		fi

# Copy the rest of the application code
COPY . .

EXPOSE 5173

# Default command runs the Vite dev server bound to all interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
