# -*- coding: utf-8 -*-

import os

import yaml

__all__ = ['source']

_DEFAULT = {
    'REGISTRY_PORT': '8080',
    'REGISTRY_HOST': '0.0.0.0',
    'SETTINGS_FLAVOR': 'dev',
    'GUNICORN_WORKERS': '1',
    'GUNICORN_GRACEFUL_TIMEOUT': '3600',
    'GUNICORN_SILENT_TIMEOUT': '3600',
    'GUNICORN_USER': '',
    'GUNICORN_GROUP': '',
    'GUNICORN_ACCESS_LOG_FILE': '"-"',
    'GUNICORN_ERROR_LOG_FILE': '"-"',
    'GUNICORN_OPTS': '[]',
    'NEW_RELIC_LICENSE_KEY': '',
    'NEW_RELIC_CONFIG_FILE': '',
    'NEW_RELIC_ENVIRONMENT': 'dev'
}


def source(key, override=''):
    # Using yaml gives us proper typage
    return yaml.load(
        os.environ.get(key, _DEFAULT[key] if key in _DEFAULT else override))
