# [Task]: T026a | [Spec]: specs/005-phase-05-cloud-native/spec.md
# Dockerfile for Next.js frontend (DigitalOcean DOKS - amd64)
# Using node:22-slim instead of alpine due to lightningcss native module issues

# Build stage
FROM node:22-slim AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (use ci for reproducible builds)
RUN npm ci --legacy-peer-deps

# Rebuild native modules for Linux (lightningcss requires this)
RUN npm rebuild lightningcss

# Copy source code
COPY . .

# Set the API URL for build time (empty = use relative URLs through ingress)
ENV NEXT_PUBLIC_API_URL=""

# Build the application (disable Turbopack - use webpack for native module compatibility)
RUN npx next build --no-turbopack

# Production stage
FROM node:22-slim AS runner

WORKDIR /app

# Set to production
ENV NODE_ENV=production

# Create non-root user for security
RUN groupadd --system --gid 1001 nodejs && \
    useradd --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Set ownership
RUN chown -R nextjs:nodejs /app

USER nextjs

# Expose port
EXPOSE 3000

# Health check (use curl instead of wget on debian-based images)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/', (r) => process.exit(r.statusCode === 200 ? 0 : 1))" || exit 1

# Run the application
CMD ["node", "server.js"]
