import stripe
from configuracion import local_settings
from django.urls import reverse

def guardar_tarjeta(user):
    stripe.api_key = local_settings.STRIPE_API_KEY
    # session = stripe.checkout.Session.create(
    # payment_method_types=['card'],
    # mode='setup',
    # customer=usuario_id,
    # success_url = 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
    #    cancel_url = 'https://example.com/cancel',
    # )
    CHECKOUT_SESSION = stripe.checkout.Session.create(
        customer=user.datosextrauser.id_customer_stripe,
        locale='es',
        metadata={
            'user_pk': user.pk,
        },
        mode='setup',
        success_url=local_settings.URL_SERVER + reverse('pago_correcto'),
        cancel_url=local_settings.URL_SERVER + reverse('pago_cancelado'),
        payment_method_types=['card'],
    )
    return CHECKOUT_SESSION

def borrar_metodo_pago(payment_method_id):
    """
    funcion para borrar un metodo de pago
    :param payment_method_id:
    :return:
    """
    stripe.api_key = local_settings.STRIPE_API_KEY
    stripe.PaymentMethod.detach(payment_method_id)

def get_tarjetas(user):
    """
    funcion para mostrar las tarjetas de un usuario
    :param user:
    :return:
    """
    stripe.api_key = local_settings.STRIPE_API_KEY
    listado = stripe.PaymentMethod.list(
        customer=user.datosextrauser.id_customer_stripe,
        type="card",
    )

    return listado

def borrar_todos_metodos_pago(user):
    listado = get_tarjetas(user)
    for pm in listado:
        borrar_metodo_pago(pm['id'])