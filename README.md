# Vpack

A package containing a lot of useful utilities for Python developing and debugging.

## Features

- Sigview: print the current running information when Ctrl+C is pressed.

## Installation

```bash
pip install vpack
```

## Examples

### Sigview

Sigview is a signal handler. It will print the current running information (e.g. file, lineno, code) when Ctrl+C is pressed.

Enable sigview:

```python
from vpack import sigview
sigview.enable()
# your code goes here
```

Now run your script and you will see the following output:
```
$ python examples/sigview_example.py
(vpack): sigview enabled. Press ^C to see the current frame. Press ^C again to exit.
1
2
1
```

Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to see the current frame.

Possible output:
```
# ...
1
2
(vpack): examples/sigview_example.py:12 in main
(vpack):         time.sleep(2)
1
2
# ...
```

Press <kbd>Ctrl</kbd> + <kbd>C</kbd> twice (in 0.5 seconds) to exit.
