sudo pip3 install -r requirements.txt
sudo cp agents_mc21.conf /etc/supervisor/conf.d/
sudo cp agents_mc21_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d mc21.medsenger.ru
touch config.py