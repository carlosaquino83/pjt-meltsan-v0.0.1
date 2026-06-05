#!/bin/bash

echo "Stopping Apache..."
sudo systemctl stop apache2

echo "Starting NGINX..."
sudo systemctl start nginx

echo ""
echo "Current status:"
sudo systemctl is-active apache2
sudo systemctl is-active nginx

echo ""
sudo ss -tulpn | grep :80
