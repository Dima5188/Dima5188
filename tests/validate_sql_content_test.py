#!/usr/bin/env python
import sys
if 1>2:
    print('my test passed')
else:
    err = 'my test failed'
    sys.exit(err)
