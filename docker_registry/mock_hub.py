# -*- coding: utf-8 -*-

import flask
import logging

from docker_registry.core import compat
from docker_registry.core import exceptions
json = compat.json

from . import toolkit

from .app import app

logger = logging.getLogger(__name__)

"""mock hub
"""

lastToken = ''
# busybox image ids
busyboxData = [{"id": "511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158"}, {"id": "7fa0dcdc88de9c8a856f648c1f8e0cf8141a505bbddb7ecc0c61f1ed5e086852"}, {"id": "ef872312fe1bbc5e05aae626791a47ee9b032efa8f3bda39cc0be7b56bfe59b9"}]

def generate_headers(namespace, repository, access):
    registry_endpoints = "0.0.0.0:5000"
    # The token generated will be invalid against a real Index behind.
    token = 'signature={0},repository="{1}/{2}",access={3}'.format(
            toolkit.gen_random_string(), namespace, repository, access)
    global lastToken
    lastToken = token
    print "lastToken"+lastToken
    return {'X-Docker-Endpoints': registry_endpoints,
            'WWW-Authenticate': token,
            'X-Docker-Token': token}

@app.route('/v1/users', methods=['GET', 'POST'])
@app.route('/v1/users/', methods=['GET', 'POST'])
def get_post_users():
    if flask.request.method == 'GET':
        return toolkit.response('OK', 200)
    try:
        # Note(dmp): unicode patch
        json.loads(flask.request.data.decode('utf8'))
    except ValueError:
        return toolkit.api_error('Error Decoding JSON', 400)
    return toolkit.response('User Created', 201)


# @app.route('/v1/users/<username>/', methods=['PUT'])
# def put_username(username):
#     return toolkit.response('', 204)


# def update_index_images(namespace, repository, data_arg):
#     path = store.index_images_path(namespace, repository)
#     sender = flask.current_app._get_current_object()
#     try:
#         images = {}
#         # Note(dmp): unicode patch
#         data = json.loads(data_arg.decode('utf8')) + store.get_json(path)
#         for i in data:
#             iid = i['id']
#             if iid in images and 'checksum' in images[iid]:
#                 continue
#             i_data = {'id': iid}
#             for key in ['checksum']:
#                 if key in i:
#                     i_data[key] = i[key]
#             images[iid] = i_data
#         data = images.values()
#         # Note(dmp): unicode patch
#         store.put_json(path, data)
#         signals.repository_updated.send(
#             sender, namespace=namespace, repository=repository, value=data)
#     except exceptions.FileNotFoundError:
#         signals.repository_created.send(
#             sender, namespace=namespace, repository=repository,
#             # Note(dmp): unicode patch
#             value=json.loads(data_arg.decode('utf8')))
#         store.put_content(path, data_arg)


# @app.route('/v1/repositories/<path:repository>', methods=['PUT'])
# @app.route('/v1/repositories/<path:repository>/images',
#            defaults={'images': True},
#            methods=['PUT'])
# @toolkit.parse_repository_name
# @toolkit.requires_auth
# def put_repository(namespace, repository, images=False):
#     data = None
#     try:
#         # Note(dmp): unicode patch
#         data = json.loads(flask.request.data.decode('utf8'))
#     except ValueError:
#         return toolkit.api_error('Error Decoding JSON', 400)
#     if not isinstance(data, list):
#         return toolkit.api_error('Invalid data')
#     update_index_images(namespace, repository, flask.request.data)
#     headers = generate_headers(namespace, repository, 'write')
#     code = 204 if images is True else 200
#     return toolkit.response('', code, headers)


@app.route('/v1/repositories/<path:repository>/images', methods=['GET'])
@toolkit.parse_repository_name
def get_repository_images(namespace, repository):
    auth = flask.request.headers.get('Authorization', '')
    print flask.request.headers
    if auth == '':
        return toolkit.response(None, 401, None)
    parts = auth.split(' ')
    if parts[0].lower() == 'token':
        print "token auth"
        print parts[1]
        print lastToken
        if len(parts) < 2 or parts[1] != lastToken:
            return toolkit.response(None, 403, None)
        return toolkit.response(busyboxData, 200, None)
    elif parts[0].lower() == 'basic':
        print "basic auth"
        headers = generate_headers(namespace, repository, 'read')
        # print "return headers %s", headers
        return toolkit.response(busyboxData, 200, headers)
    return toolkit.response(None, 401, None)


# @app.route('/v1/repositories/<path:repository>/images', methods=['DELETE'])
# @toolkit.parse_repository_name
# @toolkit.requires_auth
# def delete_repository_images(namespace, repository):
#     # Does nothing, this file will be removed when DELETE on repos
#     headers = generate_headers(namespace, repository, 'delete')
#     return toolkit.response('', 204, headers)
#
#
# @app.route('/v1/repositories/<path:repository>/auth', methods=['PUT'])
# @toolkit.parse_repository_name
# def put_repository_auth(namespace, repository):
#     return toolkit.response('OK')
