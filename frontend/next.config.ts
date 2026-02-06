import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  typescript: {
    ignoreBuildErrors: false,
  },
  // Enable standalone output for Docker deployment
  output: 'standalone',
  // Proxy /api/* requests to backend service (DOKS cluster-internal routing)
  // This allows the frontend LoadBalancer to be the single entry point
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.INTERNAL_API_URL || 'http://backend:8000'}/api/:path*`,
      },
    ]
  },
}

export default nextConfig
