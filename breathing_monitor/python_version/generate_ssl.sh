#!/bin/bash

# Generate SSL certificates for HTTPS mobile access
echo "🔒 Generating SSL certificates for HTTPS mobile access..."

# Generate private key and certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "✅ SSL certificates generated successfully!"
echo "📱 You can now access the mobile interface via HTTPS:"
echo "   https://localhost:5000/mobile"
echo ""
echo "⚠️  Note: You may need to accept the self-signed certificate in your browser."
echo "   On iPhone Safari, tap 'Advanced' and then 'Proceed to localhost'"
