import SCons.Builder
import SCons.Tool

import os
import os.path
import sys
import logging

from pyplusplus import module_builder
from pygccxml.parser.directory_cache import directory_cache_t

#def script_name(env):
#    return 'wrappers' if not env.has_key('PYPP_SCRIPT') else env['PYPP_SCRIPT']

def import_wrappers(target, source, env):

    path = None
    
    for fileName in source:
        if str(fileName).endswith('.py'): 
            path = str(fileName)
            break

    name, ext = os.path.splitext(os.path.basename(path));

    old_path = sys.path
    sys.path.append(os.path.dirname(path))
    script = __import__(name, globals())
    sys.path = old_path
    return script

def get_wrapper_node(path, env):
    path = str(path)
    className, ext = os.path.splitext(os.path.basename(path))
    return env.File(os.path.join(os.path.dirname(path), className + '.pypp.cpp'))

def generated_files(target, source, env):
    path = os.path.dirname(str(target))
    return [get_wrapper_node(os.path.join(path, os.path.basename(str(fileName))), env) for fileName in source if not str(fileName).endswith('.py')]

def modify_targets(target, source, env):
    target[0] = str(target[0]) + '.main.cpp'
    target.extend(generated_files(target, source, env))
    return target, source

def build_function(target, source, env):
    # prepare configuration
    sources = [str(path) for path in source if not str(path).endswith('.py')]
    include_paths = [str(env.Dir(path)) for path in env['CPPPATH']]
    module_name, ext = os.path.splitext(os.path.basename(str(target[0])))
    module_name = module_name[:-5]

    # initialize module builder
    mb = module_builder.module_builder_t(files=sources, include_paths=include_paths, cache=directory_cache_t())
    module_builder.set_logger_level(logging.ERROR)

    # import module declarations script
    script = import_wrappers(target, source, env)
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
