FROM php:8.0-apache

# Install system tools
RUN apt-get update && apt-get install -y \
    iputils-ping \
    whois \
    dnsutils \
    default-mysql-client \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Enable Apache modules
RUN a2enmod rewrite

# Set permissions
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

CMD ["apache2-foreground"]
