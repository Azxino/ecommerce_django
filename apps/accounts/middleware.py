# Middleware que evita que el navegador guarde páginas en caché
# Esto impide que usuarios puedan volver con el botón "atrás" después de cerrar sesión
from django.utils.deprecation import MiddlewareMixin


class NoCacheMiddleware(MiddlewareMixin):
    """
    Agrega cabeceras HTTP para evitar que el navegador cachee las páginas.
    Así, cuando el usuario cierra sesión y presiona "atrás",
    el navegador solicita la página al servidor (en lugar de mostrar la copia en caché)
    y el servidor redirige al login si el usuario ya no está autenticado.
    """

    def process_response(self, request, response):
        # Agrega cabeceras anti-caché a todas las respuestas HTTP
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
