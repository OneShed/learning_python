#!/usr/bin/env python
'''
Parse ClearCase data collected in DataDir into DestDir as JSON and CSV files

Load datasets from DataDir (populated by collect.py script) and in DestDir
directory generate individual files for each dataset:
    * regions.{csv,json}
    * clients.{csv,json}
    * vobs.{csv,json}
    * views.{csv,json}

JSON files will contain all parsed fields, while fileds for CSV files are
hardwired into this script. JSON content is prettyfied by default.
'''
import argparse
import csv
import json
import logging
import os
import re
import sys

FIELDS = {
        # key_in_parsed_data: (fields to output)
        'regions': (
            'tag',
            'comment',
            ),
        'clients': (
            'client',
            'registry_region',
            'product',
            'operating_system',
            'registry_host',
            'license_host',
            'hardware_type',
            'last_license_access',
            'last_registry_access',
            ),
        'views': (
            'region',
            'tag',
            'server_host',
            'global_path',
            'view_tag_uuid',
            'view_uuid',
            'view_attributes',
            'view_on_host',
            'view_server_access_path',
            'view_owner',
            'active',
            'comment',
            'owner',
            'group',
            'other',
            'additional_groups',
            'created',
            'created_by',
            'last_accessed',
            'last_accessed_by',
            'last_modified',
            'last_modified_by',
            ),
        'vobs': (
            'region',
            'tag',
            'server_host',
            'global_path',
            'vob_tag_replica_uuid',
            'vob_replica_uuid',
            'vob_family_uuid',
            'vob_on_host',
            'vob_server_access_path',
            'access',
            'active',
            'comment',
            'mount_options',
            ),
        }


def main(args):
    def datafilename(name, ext='json'):
        return os.path.join(args.destdir, '{}.{}'.format(name, ext))

    if not args.destdir:
        args.destdir = args.datadir

    logging.info('parsing {} ...'.format(args.datadir))
    data = parse(args.datadir)

    os.makedirs(args.destdir, exist_ok=True)
    for key, fields in FIELDS.items():
        # JSON is easy, dump what we have
        filename = datafilename(key, ext='json')
        logging.info('saving {} ...'.format(filename))
        with open(filename, 'w') as f:
            json.dump(data[key], f, sort_keys=True, indent=4)

        # CSV output only predefined fields
        filename = datafilename(key, ext='csv')
        logging.info('saving {} ...'.format(filename))
        logging.debug('fields: {}'.format(fields))
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fields, extrasaction='ignore')
            writer.writeheader()
            for row in data[key]:
                writer.writerow(row)


def parse_arguments():
    # return parsed arguments
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=__doc__)

    parser.add_argument('datadir', metavar='DataDir', type=str,
            help='Directory with collected data')
    parser.add_argument('destdir', metavar='DestDir', type=str, nargs='?',
            help='Directory where JSON and CSV files will be generated')
    parser.add_argument('--debug', '-d',
            help='Print lots of debugging statements',
            action='store_const',dest='loglevel',const=logging.DEBUG,
            default=logging.WARNING)
    parser.add_argument('--verbose', '-v',
            help='Be verbose',
            action='store_const',dest='loglevel',const=logging.INFO)

    return parser.parse_args()


# Parsing
#

def parse(directory):
    def item(name):
        return os.path.join(directory, name)

    return {
            'regions': list(parse_regions(item('regions'))),
            'clients': list(parse_clients(item('clients'))),
            'vobs': list(parse_vobs(item('vobs'))),
            'views': list(parse_views(item('views'))),
            }


def parse_regions(dirname):
    for regionsfile in _walk_files(dirname):
        with open(regionsfile) as f:
            for line in f:
                tag, comment = _parse_tagline(line)
                yield {'tag': tag, 'comment': comment}


def parse_clients(dirname):
    for clientsfile in _walk_files(dirname):
        # read lines in file, yielding each parsed 'Client:' block
        with open(clientsfile) as f:
            buff = []
            for line in f:
                line = line.strip()
                if line.startswith('Client:') and buff:
                    yield _parse_client(buff)
                    buff = [line]
                else:
                    buff.append(line)
            if buff: # for remaining entry
                yield _parse_client(buff)


def parse_vobs(dirname):
    # generate vob dictionary for each file under dirname
    for vobfile in _walk_files(dirname):
        with open(vobfile) as f:
            yield _parse_vob(f.readlines())


def parse_views(dirname):
    for viewfile in _walk_files(dirname):
        with open(viewfile) as f:
            yield _parse_view(f.readlines())


# Utility functions

def _walk_files(dirname):
    # walk for files under dirname, may raise OSError
    def onerror(exception):
        raise exception

    for dirname, dirs, files in os.walk(dirname, onerror=onerror):
        for filename in files:
            yield os.path.join(dirname, filename)


def _regexp_keyval(keys):
    # return regexp that can be used to map '<key>: <value>' line
    regexp = r'^\s*(?P<key>{})\s*:\s*(?P<value>.*)\s*$'
    return regexp.format('|'.join(keys))


def _regexp_event(events):
    # return regexp that can be used to map '<event> <time> by <id>'
    regexp = r'^\s*(?P<event>{})\s+(?P<time>\S+)\s+by\s+(?P<id>.*)\s*$'
    return regexp.format('|'.join(events))


def _jsonize(key):
    # return JSONized key value ('Some Key' -> 'some_key')
    return key.replace(' ', '_').lower()


def _parse_client(lines):
    # return dict as parsed from 'lsclient -long' lines of a single client
    def regexp():
        keys = ["Client", "Product", "Operating system", "Hardware type",
                "Registry host", "Registry region", "License host",
                "Last registry access", "Last license access",]
        return _regexp_keyval(keys)

    d = {}
    regexp = regexp()
    for line in lines:
        match = re.match(regexp, line)
        if match:
            key, value = match.group('key', 'value')
            d[_jsonize(key)] = value

    return d


def _parse_tagline(line):
    # Retrieve tuple (tag, comment) parsed from "Tag: " line
    # Comment may be empty
    regexp = r'^\s*Tag:\s+(.*?)(?:\s+"(.*)")?\s*$'
    match = re.match(regexp, line)
    if match:
        return match.groups(default='')
    else:
        return None, None


def _parse_vob(lines):
    # return dict as parsed from lines

    def regexp():
        keys = ["Global path", "Server host", "Access", "Mount options",
                "Region", "Active", "Vob tag replica uuid", "Vob on host",
                "Vob server access path", "Vob family uuid",
                "Vob replica uuid",]
        return _regexp_keyval(keys)

    d = {}
    regexp = regexp()
    for line in lines:
        # Tag: ?
        tag, comment = _parse_tagline(line)
        if tag:
            d['tag'] = tag
            d['comment'] = comment
            continue

        # Key: Value
        match = re.match(regexp, line)
        if match:
            key, value = match.group('key', 'value')
            d[_jsonize(key)] = value
            continue

    return d


def _parse_view(lines):
    # return dict as parsed from lines

    def regexp_keyval():
        keys = [
                "Active", "Additional groups", "Global path", "Group",
                "Other", "Owner", "Region", "Server host", "Tag",
                "View attributes", "View on host", "View owner",
                "View server access path", "View tag uuid", "View uuid",
                ]
        return _regexp_keyval(keys)

    def regexp_event():
        events = ['Created', 'Last modified', 'Last accessed']
        return _regexp_event(events)

    d = {}
    re_keyval, re_event = regexp_keyval(), regexp_event()
    for line in lines:
        # Tag: ?
        tag, comment = _parse_tagline(line)
        if tag:
            d['tag'] = tag
            d['comment'] = comment
            continue

        # Key: Value
        match = re.match(re_keyval, line)
        if match:
            key, value = match.group('key', 'value')
            d[_jsonize(key)] = value
            continue

        # Event fields
        match = re.match(re_event, line)
        if match:
            event, time, identity = match.group('event', 'time', 'id')
            # save it as event and event_by, sic
            key, key_by = _jsonize(event), _jsonize(event+'_by')
            d[key] = time
            d[key_by] = identity
            continue

    return d


if __name__ == '__main__':
    args = parse_arguments()
    logging.basicConfig(level=args.loglevel)
    main(args)
