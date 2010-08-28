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
	
def urllib_reporthook(bytes_read, blocks_size, total_size):
	if bytes_read != 0:
		percentage = int((float(bytes_read) / total_size) * 100)
		progress_bar = '.' * (percentage / 10) + ' ' * (10 - (percentage / 10))
		print ("\r %s %d%%" % (progress_bar, percentage)),
	
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
		response = raw_input("File %s already exists. Do you want to download it again? (y/n)" % filename)
		if response != 'y':
			return tempname
			
	tempname, headers = urllib.urlretrieve(baseurl + filename, tempname, urllib_reporthook)
	
	return tempname
	
def download_and_extract(baseurl, filename, dest):
	tempname = download(baseurl, filename)
	print "Extracting %s" % tempname
	extract_archive(tempname, dest)

def init_ext():
	print "Initializing ext/ directory"
	dirs = ['ext', 'ext/bin', 'ext/doc', 'ext/include', 'ext/lib']
	
	for path in dirs:
		if not os.path.exists(path):
			os.mkdir(path)

def install_scons():
	scons_path = os.path.join(sys.prefix, 'lib/site-packages/scons-' + SCONS_VERSION)
	
	if os.path.exists(scons_path):
		sys.path.append(scons_path)
		
	if module_exists('SCons'):
		print "SCons already installed"
		return 
		
	print "SCons not installed"
		
	tempname = download("http://prdownloads.sourceforge.net/scons/",  "scons-%s.win32.exe" % SCONS_VERSION)
	
	print "Installing SCons"
	
	# run installer
	os.system(tempname)
	
def install_boost():
	if os.path.exists('ext/include/boost'):
		print "Boost already installed"
		return
	
	boost_url = 'http://switch.dl.sourceforge.net/project/boost/boost-binaries/' + BOOST_VERSION +'/'
	boost_lib_version = BOOST_VERSION[:BOOST_VERSION.rfind('.')].replace('.', '_')
		
	print "Installing Boost libraries"

	for lib in BOOST_LIBS:
		download_and_extract(boost_url, 'boost_%s-vc90-mt-%s.zip' % (lib, boost_lib_version), 'ext/lib')
		download_and_extract(boost_url, 'boost_%s-vc90-mt-gd-%s.zip' % (lib, boost_lib_version), 'ext/lib')
		
	download_and_extract(boost_url, 'boost_%s_headers.zip' % boost_lib_version, 'ext/include')
	
def install_osg():
	if os.path.exists('ext/include/osg'):
		print "OSG already installed"
		return
		
	osg_folder = 'OpenSceneGraph-' + OSG_VERSION if OSG_VERSION.count('.') == 1 else OSG_VERSION[:OSG_VERSION.rfind('.')]
	osg_url = 'http://www.openscenegraph.org/downloads/stable_releases/OpenSceneGraph-' + osg_folder + '/binaries/Windows/VisualStudio9/'
	
	print "Installing OSG libraries"
	
	for dist in ['Debug', 'Release']:
		download_and_extract(osg_url, 'openscenegraph-all-%s-win32-x86-vc90sp1-%s.tar.gz' % (OSG_VERSION, dist), 'ext/')

	# cleanup after extract
	print "Moving OSG files"
	download_dir = 'ext/OpenSceneGraph-' + OSG_VERSION
	for dir in ['include', 'bin', 'lib']:
		for path in os.listdir(os.path.join(download_dir, dir)):
			print "\t" + path
			shutil.move(os.path.join(download_dir, dir, path), os.path.join('ext', dir))
		
	shutil.rmtree(download_dir)
		

init_ext()
install_scons()
install_boost()
install_osg()

raw_input("Installation complete, press Enter to continue")