FROM php:8.0-apache
RUN apt-get update && apt-get install -y iputils-ping whois dnsutils net-tools curl wget \
    && docker-php-ext-install mysqli pdo pdo_mysql \
    && a2enmod rewrite
EXPOSE 80
CMD ["apache2-foreground"]