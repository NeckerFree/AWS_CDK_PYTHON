#!/bin/sh
sudo apt install apache2 -y
sudo ufw allow 'Apache'
sudo systemctl status apache2
