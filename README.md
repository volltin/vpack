# Vpack

A package containing a lot of useful utilities for Python developing and debugging.

## Features

- Sigview: print the current running information when a signal is received.

## Installation

```bash
pip install vpack
```

## Examples

### Sigview

Sigview is a signal handler. It will print the current running information (e.g. file, code, line) when you send a SIGUSR1 signal to the process.

Enable sigview in your scripts:

```python
from vpack import sigview
sigview.enable()

# your code
import time
def main():
    while True:
        print('1')
        time.sleep(1) # A
        print('2')
        time.sleep(2) # B

if __name__ == '__main__':
    main()
```

Now run your script and you will see the following output:
```
sigview enabled. pid=11786, saved pid to /tmp/.sigview.pid, cmd to /tmp/.sigview.cmd
1
2
1
2
```

Create a new terminal and run the following command:
```bash
kill -s SIGUSR1 $(cat /tmp/.sigview.pid)
# or
source /tmp/.sigview.cmd
```

Possible output:
```
# ...
1
2
===  Sigview  ===
test.py:12 in main
        time.sleep(2)
=== /Sigview  ===
1
2
# ...
```


