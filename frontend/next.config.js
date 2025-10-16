const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  webpack: (config, { isServer }) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, 'src'),
    }
    
    // Ensure proper module resolution
    config.resolve.modules = [
      path.resolve(__dirname, 'src'),
      'node_modules'
    ]
    
    return config
  },
}

module.exports = nextConfig
