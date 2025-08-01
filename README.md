In de settings.py (Ip aanpassen)


sudo nano /etc/systemd/system/kapperapp.service
-----------------------------------------------
-->	Zeker de static en media goed formuleren
--> Voor gunicorn background service


[Unit]
Description=Gunicorn instance to serve kapperapp
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/kapperapp/Kapapp
ExecStart=/home/ubuntu/kapperapp/Kapapp/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/kapperapp/Kapapp/kappera>ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
Restart=on-failure
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target





/etc/nginx/sites-available/kapperapp	
-------------------------------------
-->	Eerst zonder https, dus zonder poort 443
--> IP aanpassen


server {
    if ($host = www.hairapp.be) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = hairapp.be) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    listen [::]:80;
    server_name hairapp.be www.hairapp.be 16.171.138.211;
    return 404; # managed by Certbot

}






/etc/nginx/sites-available/kapperapp
-------------------------------------
--> Dit is voor "NGINX" Bij gebruik certbot, komt er dee ssl-certs bij.


server {
    server_name hairapp.be www.hairapp.be 16.171.138.211;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ubuntu/kapperapp/Kapapp/staticfiles/;
    }
    location /media/ {
        alias /home/ubuntu/kapperapp/Kapapp/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/kapperapp/Kapapp/kapperapp/kapperapp.sock;
    }

    listen 443 ssl; # managed by Certbot
    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/hairapp.be/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/hairapp.be/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}



sudo systemctl daemon-reload

sudo systemctl restart kapperapp.service	 
-->(naam belangrijk van de gunircorn )

sudo systemctl restart nginx



Certbot
--------

sudo snap install core 
sudo snap refresh core 
sudo snap install --classic certbot 
sudo ln -s /snap/bin/certbot /usr/bin/certbot


2x  A records ( @ en www ) (2-4 uur)
sudo certbot --nginx -d hairapp.be -d www.hairapp.be
sudo certbot renew --dry-run

--> testen renew
sudo systemctl status snap.certbot.renew.timer



Check Certificate Status:
See when your certificates expire:
-->  sudo certbot certificates

Monitor Renewal Logs:
If you want to see renewal activity:
-->  sudo journalctl -u snap.certbot.renew.service

