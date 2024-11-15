#!/bin/sh
sudo apt update
sudo apt install docker-compose -y
sudo apt install git
git clone https://github.com/MiguelRamire/FinalTele.git
cd FinalTele
sudo docker-compose up -d
