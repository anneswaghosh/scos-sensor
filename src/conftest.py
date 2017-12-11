import pytest
from django.test.client import Client

import actions
import actions.tests.mocks.usrp
import scheduler
from authentication.models import User


def pytest_addoption(parser):
    parser.addoption("--testlive", action="store_true",
                     help="also run deterministic tests on live system")


@pytest.fixture
def testlive(request):
    return request.config.getoption("--testlive")


@pytest.yield_fixture
def testclock():
    real_timefn = scheduler.scheduler.utils.timefn
    real_delayfun = scheduler.utils.delayfn
    scheduler.utils.timefn = scheduler.tests.utils.TestClock()
    scheduler.utils.delayfn = scheduler.tests.utils.delayfn
    yield scheduler.utils.timefn
    scheduler.utils.timefn = real_timefn
    scheduler.utils.delayfn = real_delayfun


@pytest.fixture
def user(db):
    """A normal user."""
    username = 'test'
    password = 'password'

    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password(password)
        user.save()

    user.password = password

    return user


@pytest.fixture
def user_client(db, user):
    """A Django test client logged in as a normal user"""
    client = Client()
    client.login(username=user.username, password=user.password)

    return client


@pytest.fixture
def alternate_user(db):
    """A normal user."""
    username = 'alternate_test'
    password = 'password'

    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password(password)
        user.save()

    user.password = password

    return user


@pytest.fixture
def alternate_user_client(db, alternate_user):
    """A Django test client logged in as a normal user"""
    client = Client()
    client.login(
        username=alternate_user.username, password=alternate_user.password)

    return client


@pytest.fixture
def alternate_admin_user(db, django_user_model, django_username_field):
    """A Django admin user.
    This uses an existing user with username "admin", or creates a new one with
    password "password".
    """
    UserModel = django_user_model
    username_field = django_username_field

    try:
        user = UserModel._default_manager.get(
            **{username_field: 'alternate_admin'})
    except UserModel.DoesNotExist:
        extra_fields = {}

        if username_field != 'username':
            extra_fields[username_field] = 'alternate_admin'

        user = UserModel._default_manager.create_superuser(
            'alternate_admin', 'alternate_admin@example.com', 'password',
            **extra_fields)

    return user


@pytest.fixture
def alternate_admin_client(db, alternate_admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.login(username=alternate_admin_user.username, password='password')

    return client


mock_antenna = {
    "scos:antenna": {
        "model": "COMTELCO BS698XL3",
        "type": "dipole",
        "low_frequency": 698000000.0,
        "high_frequency": 896000000.0,
        "gain": 5.15,
        "horizontal_beam_width": 360,
        "vertical_beam_width": 30,
        "steerable": False,
        "mobile": True
    }
}

# Add mock acquisitions for tests
mock_acquire = actions.acquire_single_freq_fft.SingleFrequencyFftAcquisition(
    frequency=1e9,    # 1 GHz
    sample_rate=1e6,  # 1 MSa/s
    fft_size=16,
    nffts=11,
    antenna=mock_antenna
)
mock_acquire.usrp = actions.tests.mocks.usrp

actions.by_name['mock_acquire'] = mock_acquire
actions.init()
