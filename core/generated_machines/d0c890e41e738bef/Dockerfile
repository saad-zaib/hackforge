FROM php:8.0-apache

# Enable Apache modules
RUN a2enmod rewrite

# Create upload directory
RUN mkdir -p /var/www/html/uploads && chown www-data:www-data /var/www/html/uploads

# Set permissions
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

CMD ["apache2-foreground"]
