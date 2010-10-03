import sys
import os
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
env = Environment(variables = vars, toolpath=['#/build/tools'], tools=['default', 'findsources'], ENV = os.environ)

# performance tuning
env.Decider('MD5-timestamp')
env.SetOption('max_drift', 1)

# add command line options description
Help(vars.GenerateHelpText(env))

# configure environment for platform
debug_env, release_env = SConscript(os.path.join(buildDir, 'SConscript'), exports=['env', 'buildDir'])

targets = {'spt': list()}
# common library
for env in [debug_env, release_env]:
    # export environment and build dir for other scripts    
    Export('env')
    SConscript('src/SConscript', variant_dir = os.path.join(env['BUILD_DIR']), duplicate = 0)
    targets['spt'].append(SConscript('applications/spt/SConscript', variant_dir = os.path.join(env['BUILD_DIR'], 'applications/spt'), duplicate = 0))

# python wrappers
# if 'wrappers' in COMMAND_LINE_TARGETS:
# SConscript('wrappers/SConscript', variant_dir = os.path.join(buildDir, 'wrappers'), duplicate = 0)

# unit tests
env = debug_env
Export('env')
tests = SConscript('tests/SConscript', variant_dir = os.path.join(buildDir, 'tests'), duplicate = 0)

# documentation
if 'doc' in COMMAND_LINE_TARGETS:
    SConscript('doc/SConscript')
    
SConscript('build/msvs/SConscript')

env.Alias('install', ['#/bin', '#/python'])
env.Alias('msvc', prj)

Default(sptClient)
