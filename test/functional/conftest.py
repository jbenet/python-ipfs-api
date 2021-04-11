# Note that this file is special in that py.test will automatically import this file and gather
# its list of fixtures even if it is not directly imported into the corresponding test case.
import pathlib

import pytest

import ipfshttpclient


TEST_DIR: pathlib.Path = pathlib.Path(__file__).parent


@pytest.fixture(scope='session')
def fake_dir() -> pathlib.Path:
	return TEST_DIR.joinpath('fake_dir')


__is_available = None
def is_available():  # noqa
	"""
	Return whether the IPFS daemon is reachable or not
	"""
	global __is_available

	if not isinstance(__is_available, bool):
		try:
			ipfshttpclient.connect()
		except ipfshttpclient.exceptions.Error:
			__is_available = False
		else:
			__is_available = True

	return __is_available


def sort_by_key(items, key="Name"):
	return sorted(items, key=lambda x: x[key])


def get_client(offline=False):
	if is_available():
		return ipfshttpclient.Client(offline=offline)
	else:
		pytest.skip("Running IPFS node required")


@pytest.fixture(scope="function")
def client():
	"""Create a client with function lifetimme to connect to the IPFS daemon.

	Each test function should instantiate a fresh client, so use this
	fixture in test functions."""
	with get_client() as client:
		yield client


@pytest.fixture(scope="function")
def offline_client():
	"""Create a client in offline mode with function lifetimme"""
	with get_client(offline=True) as client:
		yield client


@pytest.fixture(scope="module")
def module_offline_client():
	"""Create a client in offline mode with module lifetime."""
	with get_client(offline=True) as client:
		yield client


@pytest.fixture
def cleanup_pins(client):
	pinned = set(client.pin.ls(type="recursive")["Keys"])
	
	yield
	
	for multihash in client.pin.ls(type="recursive")["Keys"]:
		if multihash not in pinned:
			client.pin.rm(multihash)


@pytest.fixture
def daemon():
	"""Result replaced by plugin in `run-tests.py` with the subprocess object of
	the spawned daemon."""
	return None
