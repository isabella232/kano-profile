#!/usr/bin/env python

# functions.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import json

from kano_profile.profile import load_profile, save_profile
from kano.utils import get_user_unsudoed

from .connection import request_wrapper, content_type_json
from .session import KanoWorldSession

glob_session = None


def login(login_name, password):
    login_name = login_name.strip()
    password = password.strip()

    payload = {
        'email': login_name,
        'password': password
    }

    success, text, data = request_wrapper('post', '/auth', data=json.dumps(payload), headers=content_type_json)
    if success:
        return login_register_data(data)
    else:
        return False, 'Cannot log in, problem: {}'.format(text)


def register(email, username, password):
    email = email.strip()
    username = username.strip()
    password = password.strip()

    payload = {
        'email': email,
        'username': username,
        'password': password
    }

    success, text, data = request_wrapper('post', '/users', data=json.dumps(payload), headers=content_type_json)
    if success:
        return login_register_data(data)
    else:
        return False, 'Cannot register, problem: {}'.format(text)


def login_register_data(data):
    global glob_session

    profile = load_profile()
    profile['token'] = data['session']['token']
    profile['kanoworld_username'] = data['session']['user']['username']
    profile['kanoworld_id'] = data['session']['user']['id']
    profile['email'] = data['session']['user']['email']
    save_profile(profile)
    try:
        glob_session = KanoWorldSession(profile['token'])
        return True, None
    except Exception as e:
        return False, 'There may be a problem with our servers. Try again later. Error = {}'.format(str(e))


def is_registered():
    return 'kanoworld_id' in load_profile()


def has_token():
    return 'token' in load_profile()


def remove_token():
    profile = load_profile()
    profile.pop('token', None)
    save_profile(profile)


def remove_registration():
    profile = load_profile()
    profile.pop('token', None)
    profile.pop('kanoworld_username', None)
    profile.pop('kanoworld_id', None)
    profile.pop('email', None)
    save_profile(profile)


def login_using_token():
    global glob_session

    if not is_registered():
        return False, 'Not registered!'
    if not has_token():
        return False, 'No token!'

    try:
        profile = load_profile()
        glob_session = KanoWorldSession(profile['token'])
        return True, None
    except Exception as e:
        return False, str(e)


def sync():
    if not glob_session:
        return False, 'You are not logged in!'

    success, value = glob_session.upload_profile_stats()
    if not success:
        return False, value

    success, value = glob_session.upload_private_data()
    if not success:
        return False, value

    return True, None


def backup_content(file_path):
    if not glob_session:
        return False, 'You are not logged in!'

    return glob_session.backup_content(file_path)


def restore_content(file_path):
    if not glob_session:
        return False, 'You are not logged in!'

    return glob_session.restore_content(file_path)


def get_glob_session():
    return glob_session


def get_mixed_username():
    if is_registered():
        profile = load_profile()
        username = profile['kanoworld_username']
    else:
        username = get_user_unsudoed()
    return username


def get_token():
    try:
        return load_profile()['token']
    except Exception:
        return ''


def get_email():
    try:
        email = load_profile()['email']
    except Exception:
        email = ''
    return email