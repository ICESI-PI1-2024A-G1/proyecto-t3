import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from mixer.backend.django import mixer

from usuarios.models import Ciudad, Persona, Usuario


@pytest.fixture
def client():
    """
    Fixture function that returns a logged-in client for testing purposes.

    Returns:
        Client: A Django test client object.
    """
    user = User.objects.create_user(username='admin', password='admin')
    grupo = mixer.blend("auth.Group", name="lideres")
    user.groups.add(grupo)
    user.is_superuser = True
    user.save()

    ciudad = mixer.blend(Ciudad)

    persona = mixer.blend(Persona, ciudad=ciudad)

    usuario = Usuario.objects.create(usuario=user, persona=persona)

    c = Client()

    c.login(username='admin', password='admin')

    return c

@pytest.mark.django_db
def test_administrador_page_loads(client):
    """
    Test that the administrador page loads successfully.

    Args:
        client: The Django test client.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_administrador_page_contains_title(client):
    """
    Test to verify that the administrador page contains the expected title.

    Args:
        client: Django test client object.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert b"Lista de Usuarios" in response.content

@pytest.mark.django_db
def test_administrador_page_contains_table(client):
    """
    Test that the administrador page contains a table with specific columns.

    Args:
        client: Django test client object.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert b"<table" in response.content
    assert b"<th>Nombre</th>" in response.content
    assert b"<th>Email</th>" in response.content
    assert b"<th>Rol principal</th>" in response.content
    assert "<th>Último inicio de sesión</th>" in str(response.content, 'utf-8')
    assert b"<th>Activo</th>" in response.content
    assert b"<th>Ajustes</th>" in response.content

@pytest.mark.django_db
def test_administrador_page_contains_form(client):
    """
    Test that the administrador page contains a form.

    Args:
        client: Django test client object.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert b"<form" in response.content
    assert b"name=\"q\"" in response.content
    assert b"<input" in response.content
    assert b"type=\"text\"" in response.content
    assert b"name=\"q\"" in response.content
    assert b"src=\"/static/img/search.png\"" in response.content

@pytest.mark.django_db
def test_administrador_page_contains_search_form(client):
    """
    Test that the administrador page contains a search form.

    Args:
        client: Django test client object.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert b"<form method=\"GET\"" in response.content
    assert b"<input type=\"text\" name=\"q\"" in response.content
    assert b"<img src=\"/static/img/search.png\"" in response.content

@pytest.mark.django_db
def test_administrador_page_contains_table_headers(client):
    """
    Test that the administrador page contains the expected table headers.

    Args:
        client: Django test client object.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert b"<th>Nombre</th>" in response.content
    assert b"<th>Email</th>" in response.content
    assert b"<th>Rol principal</th>" in response.content
    assert b"<th>\xc3\x9altimo inicio de sesi\xc3\xb3n</th>" in response.content
    assert b"<th>Activo</th>" in response.content
    assert b"<th>Ajustes</th>" in response.content

@pytest.mark.django_db
def test_administrador_page_contains_new_user_button(client):
    """
    Test to check if the administrador page contains a new user button.

    Args:
        client: Django test client object.

    Returns:
        None
    """
    url = reverse('administrador')
    response = client.get(url)
    assert b"<a class=\"btn btn-primary mt-2\"" in response.content
    assert b"Nuevo usuario<img class=\"icon\" src=\"/static/img/add.webp\"" in response.content
