#!/bin/bash

echo "🚀 Building optimized Docker image for Railway..."

# Clean up previous builds
docker system prune -f

# Build with optimized settings
docker build \
  --no-cache \
  --compress \
  --squash \
  -t bitcoin-prediction-optimized \
  .

echo "📊 Image size analysis:"
docker images bitcoin-prediction-optimized --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo "✅ Build completed! Image ready for Railway deployment."
echo "💡 To deploy to Railway:"
echo "   1. Push this image to your container registry"
echo "   2. Use railway.toml configuration"
echo "   3. Or connect your GitHub repo to Railway"
