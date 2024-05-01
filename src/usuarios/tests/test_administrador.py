import pytest
from django.contrib.auth.models import Group, User
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
def test_change_state(client):
    user = User.objects.create_user(username='testuser', password='12345')
    user.is_active = True
    user.save()

    response = client.post(reverse('change_state', args=[user.username]))

    user.refresh_from_db()

    assert response.status_code == 302
    assert user.is_active == False
