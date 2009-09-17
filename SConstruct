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

AddOption('--variant')
    
# DefaultEnvironment(toolpath='#/build/site_tools')

# construct build environment
env = Environment()

# export environment and build dir for other scripts    
Export('env buildDir')

# configure environment and check dependencies platform-wise
env = SConscript(os.path.join(buildDir, 'SConscript'))

# common library
SConscript('src/SConscript')

# applications
SConscript('applications/SConscript')

# python wrappers
# SConscript('wrappers/SConscript')

# unit tests
SConscript('tests/SConscript')

# documentation
SConscript('doc/SConscript')
