import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--skipapi", action="store_true", default=False, help="skip api tests"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "api: mark test as an api test")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--skipapi"):
        skip_api = pytest.mark.skip(reason="--skipapi option was given in command")
        for item in items:
            if "api" in item.keywords:
                item.add_marker(skip_api)