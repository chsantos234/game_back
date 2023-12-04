import re

def env(key=None, default=None, **kwargs):
    config = {"filename": '.env'}
    config.update(kwargs)
    
    with open(config['filename']) as infile:
        data = {}
        for line in infile:
            line = re.sub('#.*$', '', line).strip()
            if not line:
                continue
            
            info = line.split('=')
            
            if not key:
                data[info[0]] = info[1]
                continue
            
            if info[0] == key:
                return info[1]
        if not key:
            return data
        return default