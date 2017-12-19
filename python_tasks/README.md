# ccstat - Collect ClearCase statistics

Set of scripts that will gather data about ClearCase regions, clients, views
and VOBs in a local ClearCase network and save those in a plain-text (raw)
format which is then parsed into serialized (CSV, JSON) formats.

Advanced properties of views can be gathered only from a host that has network
access to a view server hosts.

## Install

This tool require Python 3.4. No installation is required, you may directly
run the scripts:

    ccstat.cmd
    python collect.py -h
    python parse.py -h

## Batch (Windows)

Script will call both collect.py and parse.py to remove and repopulate
`RawData` and `Data` inside specified directory

    ccstat.cmd workdir

## Collect

Collect plain-text data

    python collect.py --verbose workdir/RawData

## Parse

Parse collected data into JSON and CSV:

    python parse.py --verbose workdir/RawData workdir/Data