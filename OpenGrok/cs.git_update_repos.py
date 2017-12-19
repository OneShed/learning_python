#!/bin/env python 

# Clone/fetch from repos.conf and checkout ${REV}

import sys
import os
import shutil
import subprocess
import getpass
import logging
import shutil
from optparse import OptionParser
from __builtin__ import isinstance

sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'lib'))

import github3
import git

def validate_env(name):
    if  name not in os.environ:
        print( name + ' variable not available' )
        sys.exit(1)
    return 1


def has_branch( repo, branch ):
        command="git ls-remote --heads %s" % repo
        p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, shell=False)

        std_out, std_err = p.communicate()

        if p.returncode != 0:
                raise(Exception("ls-remote failed"))

        for i in std_out.splitlines():
                if i.endswith(branch):
                        return 1

# SRC_ROOT
if validate_env('SRC_ROOT'):
    src_root=os.environ['SRC_ROOT']

# URL 
if validate_env('URL'):
    URL=os.environ['URL']

# REPOS_CONF 
if validate_env('REPOS_CONF'):
    repos_conf=os.environ['REPOS_CONF']

# REV 
if validate_env('REV'):
    rev=os.environ['REV']

def update_repo():

    file = open( repos_conf, 'r')
    text = file.read()

    for repo in text.splitlines():
        gitRepoPath = "%s/%s" % (src_root, repo)
        url = "%s/%s" % (URL, repo)

        if has_branch( url, rev):

            if os.path.isdir(gitRepoPath):
                print( 'Fetching repo ' + repo + ' to ' + src_root )
                gitRepo = git.Repo(gitRepoPath)
                origin = gitRepo.remotes.origin
                try:
                    origin.fetch()
                except:
                    print( '** Cannot fetch ***' + src_root )
                    shutil.rmtree(gitRepoPath)
                    gitRepo = git.Repo.clone_from(url, gitRepoPath)
            else:
                print( 'Cloning repo ' + repo + ' to ' + src_root )
                gitRepo = git.Repo.clone_from(url, gitRepoPath)

            try:
                print( 'Checking out origin/' + rev )
                rev_name = "origin/%s" % rev
                gitRepo.git.checkout( rev_name );
            except:
                print( '*** Cannot checkout *** ' + repo )
                shutil.rmtree(gitRepoPath)
                gitRepo = git.Repo.clone_from(url, gitRepoPath)
                gitRepo.git.checkout( rev_name );

if __name__ == '__main__':
    update_repo()
