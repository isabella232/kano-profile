#!/usr/bin/env python

# kano.profile
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from __future__ import division

import sys
import os
import grp
import json
import kano.utils as ku


def load_profile():
    data = read_json(profile_file)
    if not data:
        data = dict()

    if 'username_linux' not in data:
        data['username_linux'] = linux_user

    if 'email' not in data and get_email_from_disk():
        data['email'] = get_email_from_disk()

    if 'device_id' not in data and ku.get_device_id():
        data['device_id'] = ku.get_device_id()

    if 'mac_addr' not in data and ku.get_mac_address():
        data['mac_addr'] = ku.get_mac_address()

    return data


def save_profile(data):
    data['last_save_date'] = ku.get_date_now()
    write_json(profile_file, data)


def get_email_from_disk():
    kano_email_file = os.path.join(home_directory, '.useremail')
    return ku.read_file_contents(kano_email_file)


def get_app_dir(app_name):
    app_dir = os.path.join(apps_dir, app_name)
    ku.ensure_dir(app_dir)
    return app_dir


def get_app_data_dir(app_name):
    data_str = 'data'
    app_data_dir = os.path.join(get_app_dir(app_name), data_str)
    ku.ensure_dir(app_data_dir)
    return app_data_dir


def get_app_state_file(app_name):
    app_state_str = 'state.json'
    app_state_file = os.path.join(get_app_dir(app_name), app_state_str)
    return app_state_file


def load_app_state(app_name):
    app_state_file = get_app_state_file(app_name)
    app_state = read_json(app_state_file)
    if not app_state:
        app_state = dict()
    return app_state


def load_app_state_variable(app_name, variable):
    data = load_app_state(app_name)
    if variable in data:
        return data[variable]


def save_app_state(app_name, data, levelUpDialogue=True):
    app_state_file = get_app_state_file(app_name)
    data['last_save_date'] = ku.get_date_now()

    if levelUpDialogue:
        old_level, _ = calculate_kano_level()

    write_json(app_state_file, data)

    if levelUpDialogue:
        new_level, _ = calculate_kano_level()
        if old_level != new_level:
            msg = "Congratulations, you've leveled up to level {}!".format(new_level)
            ku.run_cmd('zenity --info --text "{}"'.format(msg))


def save_app_state_variable(app_name, variable, value, levelUpDialogue=True):
    data = load_app_state(app_name)
    data[variable] = value
    save_app_state(app_name, data, levelUpDialogue)


def read_json(filepath, print_warning=False):
    try:
        return json.loads(ku.read_file_contents(filepath))
    except Exception:
        if print_warning:
            print "Problem with opening: {}".format(filepath)


def write_json(filepath, data):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def calculate_xp():
    allrules = read_json(rules_file)
    if not allrules:
        return -1

    points = 0

    for app, groups in allrules.iteritems():
        appstate = load_app_state(app)
        if not appstate:
            continue

        for group, rules in groups.iteritems():
            # calculating points based on level
            if group == 'level' and 'level' in appstate:
                maxlevel = int(appstate['level'])

                for level, value in rules.iteritems():
                    level = int(level)
                    value = int(value)

                    if level <= maxlevel:
                        points += value

            # calculating points based on multipliers
            if group == 'multipliers':
                for thing, value in rules.iteritems():
                    value = float(value)
                    if thing in appstate:
                        points += value * appstate[thing]

    return int(points)


def calculate_kano_level():
    level_rules = read_json(levels_file)
    if not level_rules:
        return -1

    max_level = max([int(n) for n in level_rules.keys()])
    xp_now = calculate_xp()

    for level in xrange(1, max_level + 1):
        level_min = level_rules[str(level)]

        if level != max_level:
            level_max = level_rules[str(level + 1)] - 1
        else:
            level_max = float("inf")

        if level_min <= xp_now <= level_max:
            reached_level = level
            reached_percentage = (xp_now - level_min) / (level_max + 1 - level_min)

            return int(reached_level), reached_percentage


def calculate_badges():
    badge_rules = read_json(badges_file)
    if not badge_rules:
        return

    badges = dict()
    for badge, rule in badge_rules.iteritems():
        appstate = load_app_state(rule['app'])
        variable_name = rule['variable']
        minvalue = float(rule['min'])
        if appstate and variable_name in appstate:
            if appstate[variable_name] >= minvalue:
                badges[badge] = False
                continue
        badges[badge] = True
    return badges


def get_gamestate_variables(app_name):
    allrules = read_json(rules_file)
    if not allrules:
        return list()

    groups = allrules[app_name]

    for group, rules in groups.iteritems():
        if group == 'multipliers':
            return [str(key) for key in rules.keys()]


def get_app_list(include_empty=False):
    apps = []
    allrules = read_json(rules_file)
    if not allrules:
        return apps

    for app, groups in allrules.iteritems():
        appstate = load_app_state(app)
        if not appstate and not include_empty:
            continue
        else:
            apps.append(app)

    return apps


# start
if __name__ == "__main__":
    sys.exit("Should be imported as module")

# checking kanousers group
try:
    kanogrp = grp.getgrnam('kanousers')
    kanomembers = kanogrp.gr_mem
except KeyError:
    sys.exit("kanousers group doesn't exist\nrun 'groupadd kanousers' first")

# getting linux variables
linux_user = ku.get_user()
home_directory = ku.get_home_by_username(linux_user)
module_file = os.path.realpath(__file__)
module_dir = os.path.dirname(module_file)

# check if run under kanouser (or sudo-ed kanouser)
if linux_user not in kanomembers:
    sys.exit("You are not member of kanousers group\nrun `usermod -a -G kanousers {}` first".format(linux_user))

# constructing paths of directories, files
kanoprofile_dir_str = '.kanoprofile'
kanoprofile_dir = os.path.join(home_directory, kanoprofile_dir_str)

profile_dir_str = 'profile'
profile_dir = os.path.join(kanoprofile_dir, profile_dir_str)

apps_dir_str = 'apps'
apps_dir = os.path.join(kanoprofile_dir, apps_dir_str)

profile_file_str = 'profile.json'
profile_file = os.path.join(profile_dir, profile_file_str)

levels_file = '/usr/share/kano-profile/levels.json'
rules_file = '/usr/share/kano-profile/rules.json'
badges_file = '/usr/share/kano-profile/badges.json'

if not os.path.exists(profile_file):
    profile = load_profile()
    ku.ensure_dir(profile_dir)
    save_profile(profile)

