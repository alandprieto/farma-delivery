from django.urls import path
from . import views

urlpatterns = [
    # URLs principales
    path('', views.home_page, name='home'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('comprar/<int:producto_id>/', views.procesar_compra, name='procesar_compra'),

    # URLs de seguimiento de pedidos
    path('mis-pedidos/', views.seguimiento_pedidos, name='seguimiento_pedidos'),
    path('pedido/<int:pedido_id>/', views.seguimiento_pedido, name='seguimiento_pedido'),

    # URLs de perfil y contacto
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('contacto/', views.contacto, name='contacto'),

    # URLs para repartidores
    path('repartidor/', views.panel_repartidor, name='panel_repartidor'),
    path('repartidor/aceptar/<int:pedido_id>/', views.aceptar_pedido, name='aceptar_pedido'),
    path('repartidor/entregar/<int:pedido_id>/', views.entregar_pedido_repartidor, name='entregar_pedido_repartidor'),
    path('repartidor/rechazar/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),

    # URLs para farmacias
    path('farmacia/', views.panel_farmacia, name='panel_farmacia'),
    path('farmacia/pedido/<int:pedido_id>/', views.detalle_pedido_farmacia, name='detalle_pedido_farmacia'),
    path('farmacia/pedido/<int:pedido_id>/confirmar-receta/', views.confirmar_receta_preparar, name='confirmar_receta_preparar'),
    path('farmacia/pedido/<int:pedido_id>/cancelar-receta/', views.cancelar_pedido_receta, name='cancelar_pedido_receta'),
    path('farmacia/pedido/<int:pedido_id>/entregar-repartidor/', views.entregar_al_repartidor, name='entregar_al_repartidor'),
    path('farmacia/pedido/<int:pedido_id>/listo-retiro/', views.listo_para_retiro, name='listo_para_retiro'),
    path('farmacia/inventario/producto/<int:producto_id>/actualizar-stock/', views.actualizar_stock, name='actualizar_stock'),
    path('farmacia/precios/', views.configuracion_precios, name='configuracion_precios'),
    path('farmacia/cuenta/', views.configuracion_cuenta_farmacia, name='configuracion_cuenta_farmacia'),

    # URLs de registro
    path('accounts/select_signup/', views.select_signup, name='select_signup'),
    path('accounts/signup/cliente/', views.cliente_signup, name='cliente_signup'),
    path('accounts/signup/farmacia/', views.farmacia_signup, name='farmacia_signup'),
    path('accounts/signup/repartidor/', views.repartidor_signup, name='repartidor_signup'),

    # API endpoints
    path('api/geocodificar/', views.geocodificar_direccion, name='geocodificar_direccion'),
    path('api/ubicacion/', views.actualizar_ubicacion_repartidor, name='actualizar_ubicacion_repartidor'),
    path('api/pedidos-disponibles/', views.api_pedidos_disponibles, name='api_pedidos_disponibles'),
    path('api/pedidos-activos/', views.api_pedidos_activos, name='api_pedidos_activos'),
]