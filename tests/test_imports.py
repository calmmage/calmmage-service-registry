import pytest


def test_imports():
    from calmmage_services_registry.settings import Settings

    assert Settings

    from calmmage_services_registry.service_registry import Service, ServiceRegistry

    assert Service
    assert ServiceRegistry
