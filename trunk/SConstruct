import sys
import os.path

from SCons.Errors import UserError
from build.support import GetPlatform

platform = GetPlatform()

if not platform:
    raise UserError("Unknown platform %s" % sys.platform)

# select platform
buildDir = os.path.join('build', platform);

# if we don't have scripts for platform report error
if not os.path.exists(os.path.join(buildDir, 'SConscript')):
    raise UserError("Platform %s is not supported" % platform)

vars = Variables()
vars.Add(BoolVariable('DEBUG', 'Set to build for debug', 1))
vars.Add(EnumVariable('TEST_PRINTER', 'Unit tests error printer', 'Paren', ('Xml', 'Error', 'Paren', 'Stdio', 'XUnit')))
    
# DefaultEnvironment(toolpath='#/build/site_tools')

# construct build environment
env = Environment(variables = vars)

# add command line options description
Help(vars.GenerateHelpText(env))

# configure environment and check dependencies platform-wise
env = SConscript(os.path.join(buildDir, 'SConscript'), exports=['env', 'buildDir'])

# performance tuning
env.Decider('MD5-timestamp')

conf = Configure(env)

if not conf.CheckLibWithHeader('osg', 'osg/Node', 'c++'):
	print 'OpenSceneGraph library not found'
	exit(1);
	
if not conf.CheckCXXHeader('boost/exception.hpp'):
	print 'Boost library not found'
	exit(1);

env = conf.Finish();

# setup defines and paths depending on DEBUG flag
if env['DEBUG']:
    defines = ['DEBUG']
    buildDir = os.path.join(buildDir, 'debug')
else:
    defines = ['NDEBUG']
    buildDir = os.path.join(buildDir, 'release')

env.Append(CPPDEFINES = defines)

# export environment and build dir for other scripts    
Export('env')

# common library
SConscript('src/SConscript', variant_dir = buildDir, duplicate = 0)

# applications
SConscript('applications/SConscript', variant_dir = os.path.join(buildDir, 'applications'), duplicate = 0)

# python wrappers
if 'wrappers' in COMMAND_LINE_TARGETS:
    SConscript('wrappers/SConscript', variant_dir = os.path.join(buildDir, 'wrappers'), duplicate = 0)

# unit tests
if 'check' in COMMAND_LINE_TARGETS:
	SConscript('tests/SConscript', variant_dir = os.path.join(buildDir, 'tests'), duplicate = 0)

# documentation
if 'doc' in COMMAND_LINE_TARGETS:
    SConscript('doc/SConscript')
