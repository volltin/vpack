# Vpack

A package containing a lot of useful utilities for Python developing and debugging.

## Features

- Sigview: print the current running information when Ctrl+C is pressed.
- Breakpt: set smart breakpoints conveniently.
- Reload: reload modules by names.

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
(vpack): Sigview enabled. Press ^C to see the current frame. Press ^C again to exit.
1
2
1
```

Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to see the current frame, possible outputs:
```
2
(vpack): examples/sigview_example.py:12 in main
(vpack):         time.sleep(2)
```

Press <kbd>Ctrl</kbd> + <kbd>C</kbd> twice (in 0.5 seconds) to exit.

You can also use `sigview.enable(openshell=True)` to open a new shell when Ctrl+C is pressed.

See [sigview_example.py](examples/sigview_example.py) and [sigview_openshell_example.py.md](examples/sigview_openshell_example.py) for more details.

## Breakpt

Breakpt is a convenient way to set breakpoints. `.at(n)` will try to open an interactive IPython shell when this **line** has been executed `n` times.

If IPython is not installed, it will try to use pdb.

You can use `breakpt.enable()` and `breakpt.disable()` to enable and disable breakpt.

```python
from vpack import breakpt

for i in range(10):
    print(i)
    breakpt.at(8) # break at i = 7
    breakpt.at(5) # break at i = 4

for i in range(6):
    print(i)
    if i == 2: breakpt.disable() # disable breakpt
    if i == 4: breakpt.enable() # enable breakpt
    breakpt.always() # break at i = 0, 1, 4, 5
```

See [breakpt_example.py](examples/breakpt_example.py) for more details.

### Reload

Reload modules by names, see [reload_example.py](examples/reload_example.py) for more details.
