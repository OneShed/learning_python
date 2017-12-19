#!/bin/env python
################################################################################
#
#  MODULE NAME: git_update_repos.py
#
#  DESCRIPTION: Script recursively checkouts specified versions of gts 
#               components for given project (eurex,prisma,common, ..).
#
#               To be used for OpenGrok indexing.
#
#  MODIFICATION HISTORY:
#
#    DATE      PROG.
#  DD-MMM-YYYY INIT.   SIR    MODIFICATION DESCRIPTION
#  ----------- ------- ------ --------------------------------------------------
#  10-JUN-2016 MENCVOJ XXXXXX Initial creation
################################################################################

import sys
import os
import subprocess
import getpass
import logging
import shutil
from optparse import OptionParser
from __builtin__ import isinstance

sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'lib'))
import github3
import git


def usage(argv=sys.argv):
    name = os.path.basename(sys.argv[0])
    return """
Script recursively checkouts specified versions of gts components for given project (eurex,prisma,common, ..). To be used for OpenGrok indexing.

GitHub automation using github3.py - python API.

In order to limit number of required command line arguments, please set default values using environment variables.
Following environment variables are respected:
GITHUB_URL - github ennterprise URL
GITHUB_USERNAME - user name which will be used to connect to GitHub instance
GITHUB_PASSWORD - password used for authentication
GITHUB_TOKEN - security token used for authentication

Please specify either one password or security token.  
    """.format(name=sys.argv[0])


def getDefaultConf(argv=sys.argv):
    defaults = {
        'url': 'https://github.deutsche-boerse.de',
        'username': getpass.getuser(),
        'password': None,
        'token': None,
        'config': None,
    }
    # find default configuration file
    cDir = os.path.abspath(os.path.dirname(argv[0]))
    cFile = os.path.basename(argv[0]).replace(".py", ".conf")
    # try to find conf file in ../etc dir.
    if os.path.exists(os.path.sep.join([os.path.dirname(cDir), 'etc', cFile])):
        defaults['config'] = os.path.sep.join([os.path.dirname(cDir), 'etc', cFile])
    else:
        defaults['config'] = os.path.sep.join([cDir, cFile])

    # get defaults from environment variables
    for variable in ['GITHUB_USERNAME', 'GITHUB_PASSWORD', 'GITHUB_TOKEN', 'GITHUB_URL']:
        if variable in os.environ:
            key = variable.replace('GITHUB_', '').lower()
            defaults[key] = os.environ[variable]

    return defaults

def parseArgs(argv=sys.argv):
    name = os.path.basename(argv[0])
    defaults = getDefaultConf()
    parser = OptionParser(usage=usage())
    parser.add_option("--org", action="store", type="string", dest="org", help="(Mandatory) source organization from where repo will be cloned", metavar="STR")
    parser.add_option("--prefix", action="store", type="string", dest="prefix", help="(Mandatory) prefix of the repositories", metavar="STR")
    parser.add_option("--rootDir", action="store", type="string", dest="rootDir", help="(Mandatory) path to root dir where repos will be cloned", metavar="STR")
    parser.add_option("--username", help="Username to be used for GitHub authentication. Default: " + defaults['username'], default=defaults['username'])
    parser.add_option("--password", help="Password to be used for GitHub auth.", default=defaults['password'])
    parser.add_option("--token", help="Token to be used for GitHub auth.", default=defaults['token'])
    parser.add_option("--url", help="URL of GitHub instance to connect. Default: " + defaults['url'], default=defaults['url'])
    parser.add_option("-P", "--promptforpassword", help="Prompt for password.", action='store_true', default=False)
    parser.add_option("--updateMasters", action="store_true", dest="updateMasters", help="Update all gts masters for given project (previously svn root)", default=False)
    parser.add_option("--updateActive", action="store_true", dest="updateActive", help="Update all components versions of active baselines for given project (previously svn root)", default=False)
    parser.add_option("--updateMigrated", action="store_true", dest="updateMigrated", help="Update all components versions of migrated baselines for given project (previously svn root)", default=False)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Enable verbose/debug mode", default=False)
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", help="do not print anything on output", default=False)
    (options, args) = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    if options.updateMasters + options.updateActive + options.updateMigrated != 1:
        parser.error("You need to specify exactly one of the following options --updateMasters, --updateMigrated, --updateActive")

    if not options.org or not options.prefix or not options.rootDir:
        parser.error("--org, --prefix and --rootDir are mandatory arguments")

    # handle secure prompt if required.
    if options.promptforpassword:
        options.password = getpass.getpass()

    return options, args

def main():
    name = os.path.basename(sys.argv[0])
    options, args = parseArgs(sys.argv)
    # handle logging - loglevel info should be printed logged by default.
    logging.root.setLevel(logging.INFO)
    if options.quiet:
        logging.root.setLevel(logging.CRITICAL)

    if options.verbose:
        logging.root.setLevel(logging.DEBUG)

    gh = github3.GitHubEnterprise(url=options.url, username=options.username, password=options.password, token=options.token)
    logging.info("Trying to list all repos in organization: {org} with prefix {prefix}".format(org=options.org, prefix=options.prefix))

    gitOrg = gh.organization(options.org)
    if not isinstance(gitOrg, github3.orgs.Organization):
        raise(Exception("Organization not found: {org}.".format(org=options.org)))

    # loop through all repositories in given organization, match given prefix and clone/fetch and checkout specified version(s)
    if options.updateMasters:
        logging.info("Updating all masters of gts components")

        repos = gitOrg.repositories()
        for repo in repos:
            if repo.name.startswith(options.prefix):
                remoteRepoURL = repo.clone_url
		logging.info("Repository {repository} in organization {organization} matched prefix {prefix} - clone URL: {repoURL}.".format(organization=options.org, repository=repo.name, prefix=options.prefix, repoURL=remoteRepoURL))

		# construct local path to cloned git repository
		repoDir = "{rootDir}/{prefix}-master".format(rootDir=options.rootDir, prefix=options.prefix)

		componentDirPath = repoDir + os.sep + repo.name
		tarFilePath = repoDir + os.sep + repo.name + ".tar.gz"

		#download version of the component as zip file and unpack it
		os.makedirs(componentDirPath)
		repo = gh.repository("dev", repo.name)
		repo.archive("tarball", tarFilePath, "master")
		command = "tar --strip-components=1 --directory=%s -xzf %s" % (componentDirPath, tarFilePath)
		logging.debug("Extracting tar ball %s to %s with command: %s" % (tarFilePath, componentDirPath, command))
		p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=False)
		std_out, std_err = p.communicate()
		if p.returncode != 0:
		   raise(Exception("Could not extract tar ball %s to %s" % (tarFilePath, componentDirPath)))
		os.remove(tarFilePath)

		# IF REPO CLONING WILL BE NEEDED USE FOLLOWING SNIPPET:
		#gitRepoPath = repoDir + os.sep + repo.name
		#if os.path.isdir(gitRepoPath):
		#    logging.debug("Fetching from remote origin")
		#    gitRepo = git.Repo(gitRepoPath)
		#    origin = gitRepo.remotes.origin
		#    origin.fetch()
		#else:
		#    logging.debug("Cloning new repository")
		#    gitRepo = git.Repo.clone_from(remoteRepoURL, gitRepoPath)
		# checkout given branch/tag
		#gitRepo.git.checkout("master")

    elif options.updateActive:
        # construct local path to cloned git repository and other data
        repoDir = "{rootDir}/{prefix}-open-baselines".format(rootDir=options.rootDir, prefix=options.prefix)
        product = options.prefix[len("gts."):]

        logging.info("Updating all active baselines for product %s" % product)

        # obtain all open releases for given product
        # ssh contint@otd2187 "/sw/int/prisma/toolkit/bin/rsark.py get_open_int_releases --system=eurex"
        command = "sshpass,-p,Cont 1nt,ssh,contint@otd2187,/sw/int/prisma/toolkit/bin/rsark.py,get_open_int_releases,--system=%s" % product

        logging.debug("obtain open baseline versions via command: %s" % command)
        p = subprocess.Popen(command.split(","), stdout=subprocess.PIPE, shell=False)
        std_out, std_err = p.communicate()
        if p.returncode != 0:
            raise(Exception("Could not obtain open baselines for product %s" % product))
        baselines = filter(None, (line.rstrip() for line in std_out.splitlines()))

        for baseline in baselines:
            command = "sshpass,-p,Cont 1nt,ssh,contint@otd2187,/home/contint/bin/getComponentsAndVersions.sh %s %s %s" % (product, baseline, "dev")
            logging.debug("obtain baseline components and versions by command: %s" % command)
	    print( 'Product:' + product )
	    print( 'Baseline:' + baseline )
            p = subprocess.Popen(command.split(","), stdout=subprocess.PIPE, shell=False)
            std_out, std_err = p.communicate()
            if p.returncode != 0:
                raise(Exception("Could not obtain components for product version %s-%s" % (product, baseline)))
            componentsAndVersions = filter(None, (line.rstrip() for line in std_out.splitlines()))
            for componentAndVersion in componentsAndVersions:
                component, componentVersion = componentAndVersion.split()
                componentDirPath = repoDir + os.sep + baseline + os.sep + component + "-" + componentVersion
                tarFilePath = componentDirPath + os.sep + componentVersion + ".tar.gz"

                os.makedirs(componentDirPath)

                # download version of the component as zip file and unpack it
                repo = gh.repository("dev", "gts." + component.replace("/", "."))
                repo.archive("tarball", tarFilePath, componentVersion)
                command = "tar --strip-components=1 --directory=%s -xzf %s" % (componentDirPath, tarFilePath)
                logging.debug("Extracting tar ball %s to %s with command: %s" % (tarFilePath, componentDirPath, command))
                p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, shell=False)
                std_out, std_err = p.communicate()
                if p.returncode != 0:
                    raise(Exception("Could not extract tar ball %s to %s" % (tarFilePath, componentDirPath)))
                
                os.remove(tarFilePath)
    elif options.updateMigrated:
        # construct local path to cloned git repository
        repoDir = "{rootDir}/{prefix}-migrated".format(rootDir=options.rootDir, prefix=options.prefix)
        product = options.prefix[len("gts."):]

        logging.info("Updating all migrated baselines for product %s" % product)

        releaseRepo = gh.repository("rel", options.prefix + ".release")

        # obtain all migrated baselines
        # remove all tags but release tags
	for gitTag in releaseRepo.tags():
            baseline = gitTag.name

	    #baseline = baseline.replace("release-","")
	    if "release-" in baseline:
		    continue

            command = "sshpass,-p,Cont 1nt,ssh,contint@otd2187,/home/contint/bin/getComponentsAndVersions.sh %s %s %s" % (product, baseline, "dev")
            logging.debug("obtain baseline components and versions by command: %s" % command)
            p = subprocess.Popen(command.split(","), stdout=subprocess.PIPE, shell=False)
            std_out, std_err = p.communicate()
            if p.returncode != 0:
                raise(Exception("Could not obtain components for product version %s-%s" % (product, baseline)))
            componentsAndVersions = filter(None, (line.rstrip() for line in std_out.splitlines()))
            for componentAndVersion in componentsAndVersions:
                component, componentVersion = componentAndVersion.split()
                componentDirPath = repoDir + os.sep + baseline + os.sep + component + "-" + componentVersion
                tarFilePath = componentDirPath + os.sep + componentVersion + ".tar.gz"

                os.makedirs(componentDirPath)

                # download version of the component as zip file and unpack it
                repo = gh.repository("dev", "gts." + component.replace("/", "."))
                repo.archive("tarball", tarFilePath, componentVersion)
                command = "tar --strip-components=1 --directory=%s -xzf %s" % (componentDirPath, tarFilePath)
                logging.debug("Extracting tar ball %s to %s with command: %s" % (tarFilePath, componentDirPath, command))
                p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=False)
                std_out, std_err = p.communicate()
                if p.returncode != 0:
                    raise(Exception("Could not extract tar ball %s to %s" % (tarFilePath, componentDirPath)))
                
                os.remove(tarFilePath)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt, e:
        try:
            os.kill(-(os.getpid()), 5)
        except Exception, e:
            pass
        pass
