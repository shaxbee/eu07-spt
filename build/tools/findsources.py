import SCons.Util

def FindAllSourceFiles(self, target):
    def _find_sources(tgt, src, hdr, all):
        for item in tgt:
            if SCons.Util.is_List(item):
                _find_sources(item, src, hdr, all)
            else:
                if item.abspath in all:
                    continue

                all[item.abspath] = True

                if item.path.endswith('.cpp'):
                    if not item.exists():
                        item = item.srcnode()
                    src.append(item.abspath)
                elif item.path.endswith('.h'):
                    if not item.exists():
                        item = item.srcnode()
                    hdr.append(item.abspath)
                else:
                    lst = item.children(scan=1)
                    _find_sources(lst, src, hdr, all)

    sources = []
    headers = []
    
    _find_sources(target, sources, headers, {})

    return sources, headers

def generate(env):
    from SCons.Script.SConscript import SConsEnvironment # just do this once
    SConsEnvironment.FindAllSourceFiles = FindAllSourceFiles

def exists(env):
    from SCons.Script.SConscript import SConsEnvironment
    return hasattr(SConsEnvironment, "FindAllSourceFiles")