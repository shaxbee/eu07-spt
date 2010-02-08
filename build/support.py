import sys

def GetPlatform():
    for platform in ['linux', 'win32']:
        if platform in sys.platform:
            return platform
    return None
