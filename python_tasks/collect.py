#!/usr/bin/env python
'''
Script will run several ClearCase commands to obtain data about regions,
clients, views and VOBs. In DestDir, each category will be stored in own
directory tree with individual files that contain output of 'cleartool ls...
-long ...' commands:

./regions/all
./clients/all
./vobs/${region}/${tag_safe}
./views/${region}/${tag}

Directory separators in VOB tag names are replaced in a way so that
'/vobs/foo' become 'vobs-foo' and '\\vob_foo' becomes 'vob_foo'. This ensure
that safe filenames are generated for interoperability regions (UNIX vs
Windows).

When collecting views, script will ignore any errors comming from 'cleartool'
(unreachable view server, invalid or missing view entry or timeout). View data
files which are empty are then removed.
'''

import argparse
import logging
import multiprocessing
import os
import subprocess

ALL_FILENAME = 'all'

def main(args):
    # create destination directory

    # 'all' files
    collect_regions(filename=os.path.join(
        _make_join_dirs(args.destdir, 'regions'), ALL_FILENAME))
    collect_clients(filename=os.path.join(
        _make_join_dirs(args.destdir, 'clients'), ALL_FILENAME),
        server=args.server)

    # individual entries
    if not args.regions:
        args.regions = _all_regions()

    collect_vobs(_make_join_dirs(args.destdir, 'vobs'),
            regions=args.regions,
            processes=args.processes)
    collect_views(_make_join_dirs(args.destdir, 'views'),
            regions=args.regions,
            properties=args.properties,
            full=args.full,
            timeout=args.timeout,
            processes=args.processes)


def parse_arguments():
    # return parsed arguments
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=__doc__)

    parser.add_argument('destdir', metavar='DestDir', type=str,
            help='Destination directory for collected data')

    parser.add_argument('--region', '-r', dest='regions', type=str,
            nargs='*',
            help='Collect VOBs and views from specified region(s)'
            ' (default: all)')
    parser.add_argument('--server', '-s', type=str,
            default='localhost',
            help='Server name for "lsclients -host" (default: localhost)')
    parser.add_argument('--properties', '-p', action='count',
            help='Collect view properties')
    parser.add_argument('--full', '-f', action='count',
            help='Report additional properties')
    parser.add_argument('--timeout', '-t', type=int, default=None,
            help='Timeout for "cleartool lsview" (seconds, default: none)')
    parser.add_argument('--processes', '-P', type=int, default=None,
            help='Number of processes to run in parallel (default: number'
            ' of CPUs)') # None is to autodetect # of CPUs

    parser.add_argument('-d','--debug',
            help='Print lots of debugging statements',
            action='store_const',dest='loglevel',const=logging.DEBUG,
            default=logging.WARNING
            )
    parser.add_argument('-v','--verbose',
            help='Be verbose',
            action='store_const',dest='loglevel',const=logging.INFO
            )

    return parser.parse_args()


# Collector functions

def collect_regions(filename):
    # save all regions data into destfile
    with open(filename, 'w') as f:
        _cleartool(['lsregion', '-long'], stdout=f)
    logging.info(filename)


def collect_clients(filename, server):
    # save all clients data into destdir as filename
    with open(filename, 'w') as f:
        _cleartool(['lsclient', '-long', '-host', server], stdout=f)
    logging.info(filename)


def collect_vobs(destdir, regions, processes=None):
    # save vob data into destdir, converting each tag into fs-friendly name

    # precreate directories
    for region in regions:
        regiondir = _make_join_dirs(destdir, region)
        logging.debug('created {}'.format(regiondir))

    # execute in pool
    with multiprocessing.Pool(processes=processes) as pool:
        pool.starmap(_collect_vob, _walk_vobs(regions, destdir))


def collect_views(destdir, regions, processes=None, properties=False,
        full=False,timeout=None):
    # save views data into destdir

    # precreate directories
    for region in regions:
        regiondir = _make_join_dirs(destdir, region)
        logging.debug('created {}'.format(regiondir))

    # execute in pool
    with multiprocessing.Pool(processes=processes) as pool:
        # _collect_view needs same argument order as _walk_views return
        pool.starmap(_collect_view, _walk_views(regions, destdir,
            properties=properties, full=full, timeout=timeout))


# Utility functions

def _cleartool(cmd, *args, **kwargs):
    # invoke check_call() for cleartool cmd
    subprocess.check_call(['cleartool']+cmd, *args, **kwargs)


def _cleartool_output(cmd, *args, **kwargs):
    # return decoded check_output() for cleartool cmd
    return subprocess.check_output(['cleartool']+cmd,
            *args, **kwargs).decode()


def _make_join_dirs(base, *subdirs, exist_ok=True):
    # return path to directory created as a join of base and subdirs
    path = os.path.join(base, *subdirs)
    os.makedirs(path, exist_ok=exist_ok)
    return path


def _all_regions():
    # return names of all regions known to this host
    cmd = ['lsregion', '-short']
    return _cleartool_output(cmd).splitlines()


def _walk_views(regions, topdir=None, properties=False, full=False, timeout=None):
    # generate tuples of (region, tag, filename, properties, timeout) for
    # views to be collected

    def viewtags(region):
        cmd = ['lsview', '-short', '-region', region]
        return _cleartool_output(cmd).splitlines()

    for region in regions:
        for tag in viewtags(region):
            filename = os.path.join(topdir, region, tag)
            yield region, tag, filename, properties, full, timeout


def _collect_view(region, tag, filename, properties=False, full=False, timeout=False):
    # save 'lsview -long (-properties) (-full) -region $region $tag' into filename
    # remove resulting file if it come out as empty

    def log_warning(message):
        msg = '{} for view "{}" in region "{}"'
        logging.warning(msg.format(message, tag, region))

    def lsviewcmd(tag, region):
        cmd = ['lsview', '-long', '-region', region]
        if properties:
            cmd.extend(['-properties'])
        if full:
            cmd.extend(['-full'])
        cmd.extend([tag])
        return cmd

    with open(filename, 'w') as f:
        # Command 'cleartool lsview -long -properties' may fail (or timeout)
        # when view host is not accessible. In this case stdout contain only
        # basic registry data that we keep.
        try:
            _cleartool(lsviewcmd(tag, region), stdout=f, timeout=timeout)
        except subprocess.CalledProcessError:
            log_warning('Operation lsview failed')
        except subprocess.TimeoutExpired:
            log_warning('Operation lsview timeout')

    # For fatal errors (view tag not present anymore, invalid license, etc..)
    # the output file will be empty as there would be no message on stdout
    # from 'cleartool'.
    if not os.path.getsize(filename):
        log_warning('No data collected')
        os.remove(filename) # it's empty anyway

    logging.info(filename)


def _walk_vobs(regions, topdir=None):
    # generate tuples of (region, tag, filename) for vobs to be collected
    # filename is joined topdir, region and fs-friendly tag

    def vobtags(region):
        # return list of vob-tags in region
        cmd = ['lsvob', '-short', '-region', region]
        return _cleartool_output(cmd).splitlines()

    for region in regions:
        for tag in vobtags(region):
            filename = os.path.join(topdir, region, _tag2file(tag))
            yield region, tag, filename


def _collect_vob(region, tag, filename):
    # save 'lsvob -long -region $region $tag' into filename
    with open(filename, 'w') as f:
        _cleartool(['lsvob', '-long', '-region', region, tag], stdout=f)
    logging.info(filename)


def _tag2file(tag, rep='-'):
    # remove leading slash or backslash and replace remaining ones with rep
    tag = tag.lstrip('/\\')
    tag = tag.replace('/', rep)
    tag = tag.replace('\\', rep)
    return tag


if __name__ == '__main__':
    args = parse_arguments()
    logging.basicConfig(level=args.loglevel)
    main(args)
