from django.db import models
from django.utils import timezone

# Create your models here.
class News(models.Model):
    """Modelo que representa una noticia."""
    category = models.CharField(max_length=100, verbose_name="Categoría")
    title = models.CharField(max_length=255, verbose_name="Título")
    image_url = models.URLField(max_length=500, verbose_name="URL de la imagen")
    news_url = models.URLField(max_length=500, verbose_name="URL de la noticia")
    extracted_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de extracción")
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name="Autor")

    class Meta:
        db_table = 'news'
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-extracted_at']

    def __str__(self):
        return self.title

class ProductPrice(models.Model):
    """Modelo que representa el precio de un producto."""
    product = models.CharField(max_length=150, verbose_name="Producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    variation = models.CharField(max_length=50, verbose_name="Variación")
    unit_measure = models.CharField(max_length=50, verbose_name="Unidad de medida")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de actualización")

    class Meta:
        db_table = 'product_prices'
        verbose_name = 'Precio de Producto'
        verbose_name_plural = 'Precios de Productos'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.product} - {self.price}"
