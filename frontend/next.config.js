/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8010/api',
  },
  // Para funcionar em Docker
  output: 'standalone',
};

module.exports = nextConfig;

