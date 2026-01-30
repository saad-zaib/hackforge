FROM php:8.0-apache

RUN apt-get update && apt-get install -y \
    iputils-ping whois dnsutils net-tools curl wget \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite

EXPOSE 80

CMD ["apache2-foreground"]
