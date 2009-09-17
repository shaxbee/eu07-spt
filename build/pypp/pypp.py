import SCons.Builder
import SCons.Tool

import os
import os.path
import sys
import logging

from pyplusplus import module_builder
from pygccxml.parser.directory_cache import directory_cache_t

def script_name(env):
    return 'wrappers' if not env.has_key('PYPP_SCRIPT') else env['PYPP_SCRIPT']

def import_wrappers(target, env):
    old_path = sys.path
    sys.path.append(os.path.dirname(str(target[0])))
    script = __import__(script_name(env), globals())
    sys.path = old_path
    return script

def generated_files(source):
    result = list()
    for path in source:
        className, ext = os.path.splitext(os.path.basename(str(path)))
        result.append(os.path.join(className + '.pypp.cpp'))
    return result

def modify_targets(target, source, env):
    target[0] = str(target[0]) + '.main.cpp'
    target.extend(generated_files(source))
    env.Depends(source, os.path.join(script_name(env) + '.py'))
    return target, source

def build_function(target, source, env):
    # prepare configuration
    sources = [str(path) for path in source]
    include_paths = [str(env.Dir(path)) for path in env['CPPPATH']]
    module_name, ext = os.path.splitext(os.path.basename(str(target[0])))
    module_name = module_name[:-5]

    # initialize module builder
    mb = module_builder.module_builder_t(files=sources, include_paths=include_paths, cache=directory_cache_t())
    module_builder.set_logger_level(logging.ERROR)

    # import module declarations script
    script = import_wrappers(target, env)
    script.wrap(mb)

    # write code to file
    mb.build_code_creator(module_name=module_name)
    mb.code_creator.user_defined_directories.append(os.path.dirname(str(target[0])))
    mb.code_creator.user_defined_directories.extend(include_paths)
    files = mb.split_module(os.path.dirname(str(target[0])))
    return None


def generate(env):

    print "Loading PYPP tool..."

    builder = SCons.Builder.Builder(
        action = build_function,
        emitter = modify_targets,
        src_suffix = ['.h', '.hpp'])

    env.Append(BUILDERS = {'PyPP': builder})

def exists(env):
    return env.Detect('gccxml')
