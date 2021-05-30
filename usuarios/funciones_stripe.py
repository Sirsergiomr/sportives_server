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
        success_url=local_settings.URL_SERVER + reverse('pago_correcto'),
        cancel_url=local_settings.URL_SERVER + reverse('pago_cancelado'),
        mode='setup',
        payment_method_types=['card'],
        locale='es',
        metadata={
            'user_pk': user.pk,
        },
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
    :retuºrn:
    """
    stripe.api_key = local_settings.STRIPE_API_KEY
    listado = stripe.PaymentMethod.list(
        customer=user.datosextrauser.id_customer_stripe,
        type="card",
    )

    return listado
    return CHECKOUT_SESSION
def borrar_todos_metodos_pago(user):
    listado = get_tarjetas(user)
    for pm in listado:
        borrar_metodo_pago(pm['id'])


def securepay(amount_value, transaccion):
    print(amount_value)

    if transaccion.creador.datosextrauser.id_customer_stripe is not None or transaccion.creador.datosextrauser.id_customer_stripe == '':
        metodos_pago = get_tarjetas(transaccion.creador)
        print(metodos_pago)

        try:
            pm = metodos_pago['data'][0]['id']
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_value,
                currency="eur",
                confirm=True,
                description="Sportice Titans %s - %s" % (transaccion.creador.email, amount_value),
                customer=transaccion.creador.datosextrauser.id_customer_stripe,
                metadata={'usuario_pk': transaccion.creador.pk,
                          'usuario': transaccion.creador.username,
                          'transaccion_pk': transaccion.pk,
                          'contabilizar': True},
                payment_method=pm
            )
            print(payment_intent)
            print(payment_intent['status'])

            if payment_intent['status'] == "requires_source_action":
                client_secret = payment_intent['client_secret']

                return False, {"mensaje": "Hay que verificar", "client_secret": client_secret}
            else:
                return True, "Pago realizado"

        except Exception as e:
            print(e)
            return False, {
                "mensaje": 'No podemos cobrar de su tarjeta de credito, prueba de nuevo mas tarde o intentelo con otra tarjeta de credito válida',
                "client_secret": None}
    else:
        return False, {"mensaje": 'No se ha encontrado la tarjeta, pruebe con otra tarjeta', "client_secret": None}





























