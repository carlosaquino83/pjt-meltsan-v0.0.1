#!/bin/bash

echo "Stopping NGINX..."
sudo systemctl stop nginx

echo "Starting Apache..."
sudo systemctl start apache2

echo ""
echo "Current status:"
sudo systemctl is-active nginx
sudo systemctl is-active apache2

echo ""
sudo ss -tulpn | grep :80
