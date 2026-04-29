"В демонстрационных целях используется самоподписанный SSL-сертификат. В производственной среде будет установлен сертификат Let's Encrypt с автоматическим обновлением через certbot."
## Установка Let's Encrypt (production)
1. Замените `corp-lis.ru` на ваш домен в `docker-compose.yml` и `nginx.conf`
2. Выполните команду получения сертификата:
`docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d corp-lis.ru -d www.corp-lis.ru --email admin@corp-lis.ru --agree-tos --no-eff-email`
3. Перезапустите: `docker-compose up -d`