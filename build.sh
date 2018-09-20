docker-compose build
python check_image_updates.py python 3.7
python check_image_updates.py mongo 4.1.3
read -n 1 -s -r -p "Press any key to continue"