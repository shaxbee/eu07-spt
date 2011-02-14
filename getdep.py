import sys

import os
import os.path

import urllib

import zipfile
import tarfile

import shutil

from getdep_config import *

installpath = sys.prefix
tempdir = os.environ['TEMP']

def module_exists(name):
    try:
        __import__(name, globals(), locals())
    except ImportError:
        return False
        
    return True
    
def urllib_reporthook(numblocks, blocksize, filesize):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    sys.stdout.write("\r%3d%%" % percent)

def extract_archive(filename, dest):
    archive = None
    if filename.endswith('.zip'):
        archive = zipfile.ZipFile(filename, 'r')
    elif filename.endswith('.tar.gz'):
        archive = tarfile.open(filename, 'r')
    else:
        raise RuntimeError('Unsupported "%s" archive extension' % filename)
        
    archive.extractall(dest)
    archive.close()
    
def download(baseurl, filename):
    print "Downloading %s%s" % (baseurl, filename)
    tempname = os.path.join(tempdir, filename)
    if os.path.exists(tempname):
        response = raw_input("File %s already exists. Do you want to download it again? (y/n) " % filename)
        if response != 'y':
            return tempname
            
    tempname, headers = urllib.urlretrieve(baseurl + filename, tempname, urllib_reporthook)
    print ""
    
    return tempname
    
def download_and_extract(baseurl, filename, dest):
    tempname = download(baseurl, filename)
    print "Extracting %s" % tempname
    extract_archive(tempname, dest)

def init_ext():
    print "Initializing ext/ directory"
    dirs = ['ext', 'ext/include', 'ext/lib', 'ext/bin']
    
    for path in dirs:
        if not os.path.exists(path):
            os.mkdir(path)
    
def install_boost():
    if os.path.exists('ext/include/boost'):
        print "Boost already installed"
        return

    boost_lib_version = BOOST_VERSION[:BOOST_VERSION.rfind('.')].replace('.', '_')
        
    print "Installing Boost libraries"

    for lib in BOOST_LIBS:
        download_and_extract(BOOST_URL, 'boost_%s-vc90-mt-%s.zip' % (lib, boost_lib_version), 'ext/lib')
        download_and_extract(BOOST_URL, 'boost_%s-vc90-mt-gd-%s.zip' % (lib, boost_lib_version), 'ext/lib')
        
    download_and_extract(BOOST_URL, 'boost_%s_headers.zip' % boost_lib_version, 'ext/include')
    
def install_osg():
    if os.path.exists('ext/include/osg'):
        print "OSG already installed"
        return
        
    print "Installing OSG libraries"
    
    for lib in ['libopenscenegraph',  'libopenscenegraph-dev', 'libopenthreads', 'libopenthreads-dev']:
        for dist in ['Debug', 'Release']:
            download_and_extract(OSG_URL, '%s-%s-win32-x86-vc90-%s.zip' % (lib, OSG_VERSION, dist), tempdir)

    # cleanup after extract
    print "Moving OSG files"
    download_dir = os.path.join(tempdir, 'OpenSceneGraph-' + OSG_VERSION)
    for dir in ['include', 'bin', 'lib']:
        for path in os.listdir(os.path.join(download_dir, dir)):
            shutil.move(os.path.join(download_dir, dir, path), os.path.join('ext', dir))

    shutil.rmtree(download_dir)

def install_gtest():
    if os.path.exists('ext/include/gtest'):
        print "Google Test already installed"
        return
        
    gtest_url = 'http://shaxbee.eu07.pl/spt-dep/'
    
    print "Installing Google Test"
    
    download_and_extract(gtest_url, 'gtest-%s.zip' % GTEST_VERSION, 'ext')
    
def install_editor_libs():
    if os.path.exists('applications/sptEditor/src/_sptmath.pyd'):
        print "Editor libraries already installed"
        return
    
    sptmath_url = 'http://shaxbee.eu07.pl/spt-dep/'
    
    print "Installing Editor libraries"
    
    download_and_extract(sptmath_url, 'sptmath.zip', 'applications/sptEditor/src')
    

init_ext()
install_boost()
install_osg()
install_gtest()
install_editor_libs()

raw_input("Installation complete, press Enter to continue")