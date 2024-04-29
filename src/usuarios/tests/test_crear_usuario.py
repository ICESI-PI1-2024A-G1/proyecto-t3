import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from mixer.backend.django import mixer

from usuarios.models import Ciudad, Persona, Usuario


@pytest.fixture
def client():
    from django.contrib.auth.models import Group

    Group.objects.get_or_create(name='admin')

    user = User.objects.create_user(username='admin', password='admin')
    user.is_superuser = True
    user.save()

    ciudad = mixer.blend(Ciudad)

    persona = mixer.blend(Persona, ciudad=ciudad)

    usuario = Usuario.objects.create(usuario=user, persona=persona)

    c = Client()

    c.login(username='admin', password='admin')

    return c

@pytest.mark.django_db
def test_crear_usuario_form(client):
    """
    Test the creation of a user form.

    Args:
        client: The Django test client.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 302.
    """
    response = client.post(reverse('crear_usuario'), {
        'cedula': '123456789',
        'nombre': 'Mikey',
        'apellido': 'Mouse',
        'email': 'mikey.mouse@example.com',
        'telefono': '1234567890',
        'ciudad': '1',
        'birthdate': '2022-01-01T00:00',
        'rol': 'admin'
    })

    assert response.status_code == 302

@pytest.mark.django_db
def test_crear_usuario_submit(client):
    """
    Test the submission of creating a new user.

    Args:
        client: The Django test client.

    Returns:
        None
    """
    response = client.post(reverse('crear_usuario'), {
        'cedula': '123456789',
        'nombre': 'Mikey',
        'apellido': 'Mouse',
        'email': 'mikey.mouse@example.com',
        'telefono': '1234567890',
        'ciudad': '1',
        'birthdate': '2022-01-01T00:00',
        'rol': 'admin'
    })

    assert response.status_code == 302

@pytest.mark.django_db
def test_successful_user_creation(client):
    """
    Test successful creation of a new user.

    Args:
        client: The Django test client.

    Returns:
        None
    """
    response = client.post(reverse('crear_usuario'), {
        'cedula': '123456789',
        'nombre': 'Mikey',
        'apellido': 'Mouse',
        'email': 'mikey.mouse@example.com',
        'telefono': '1234567890',
        'ciudad': '1',
        'birthdate': '2022-01-01T00:00',
        'rol': 'admin'
    })

    assert response.status_code == 302
    assert User.objects.filter(email='mikey.mouse@example.com').exists()
