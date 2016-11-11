## Usage

There are currently two functions `image_to_print` and `image_to_list`.
Both only take an image location as argument. `image_to_print` is mainly for
debugging purposes and prints nicely formatted columns, examples of the output
can be seen under [notes](#notes).

`image_to_list` returns a list containing dict(s) with the following values:

* `region`: A boolean, `True` meaning the license plate is from the Netherlands.

* `plate`: A string containing the license plate number.

* `confidence`: A float value ranging from 0 to 100 meaning how confident `openalpr` is about the plate number being correct.

Some example of `image_to_list` in use:

```
>>> example = image_to_list('./photos/1.jpg')
>>> print(example)
[{'region': True, 'confidence': 94.660286, 'plate': '37-TVR-1'}, {'region': True, 'confidence': 82.577583, 'plate': '37TYR1'}]
```

```
>>> example = image_to_list('./photos/3.jpg')
>>> print(example[0])
{'confidence': 94.939178, 'plate': '94NLD5', 'region': True}
```

```
>>> example = image_to_list('./photos/6.jpg')
>>> print(example[0]['region'])
False
```

```
>>> example = image_to_list('./photos/1.jpg')
>>> print(example[1]['plate'])
37TYR1
```

`image_to_list` returns a list with the possibility of multiple dicts instead of just returning the most confident
result (`[0]`) for the following reason:

Say you try to send the plate number to `https://overheid.io/api/voertuiggegevens/{kenteken}`
and the API returns with an error saying how the plate doesn't exist. Now because we (possibly) have
mutliple plate results you can just keep trying to send the next most confident plate number. A good
example of where this would be useful is `6.jpg` (again, see [notes](#notes)), where the correct
result is *not* the most confident plate (`[0]`), but actually `[2]`.


## Installation

This script depends on `openalpr` and its `python3` bindings.

On GNU/Linux you should just install `openalpr` using your package manager and you're ready to go.
If you use Windows you can probably download a binary from https://github.com/openalpr/openalpr/releases and drop it in your `PATH`, maybe
you need to run `vc_redist.x64.exe` and `python/setup.py` as well, oh, and try moving `openalprpy.dll` to wherever `dll` files are stored.
I'm pretty sure this is somewhere in the `windows` directory.

Full (GNU/Linux) dependency tree:

```
python3
-> sqlite3
-> -> ncurses
-> -> readline
-> expat
-> libffi
openalpr
-> opencv
-> -> cmake
-> -> -> curl
-> -> -> -> openssl
-> -> -> -> zlib
-> -> -> libarchive
-> -> -> -> bzip2
-> -> -> -> xz
-> -> -> -> acl
-> -> -> -> -> attr
-> -> -> -> lzo
-> tesseract
-> -> cairo
-> -> -> fontconfig
-> -> -> -> freetype
-> -> -> -> -> libpng
-> -> -> xorg-libxext
-> -> -> -> xorg-libx11
-> -> -> -> -> xorg-libxcb
-> -> -> -> -> -> xorg-xcb-proto
-> -> -> -> -> -> -> python
-> -> -> -> -> -> -> -> db
-> -> -> -> -> -> -> -> gdbm
-> -> -> -> -> -> xorg-libxdmcp
-> -> -> -> -> -> -> xorg-xproto
-> -> -> -> -> -> xorg-libxau
-> -> -> -> -> -> libxslt
-> -> -> -> -> -> -> libxml2
-> -> -> -> -> -> libpthread-stubs
-> -> -> -> -> xorg-xf86bigfontproto
-> -> -> -> -> xorg-xextproto
-> -> -> -> -> xorg-xtrans
-> -> -> -> -> -> xorg-util-macros
-> -> -> -> -> xorg-kbproto
-> -> -> -> -> xorg-inputproto
-> -> -> xorg-libxrender
-> -> -> -> xorg-renderproto
-> -> -> xorg-libpixman
-> -> -> xorg-xcb-util
-> -> -> glib
-> -> -> -> libpcre
-> -> icu
-> -> pango
-> -> -> harfbuzz
-> -> -> xorg-libsm
-> -> -> -> xorg-libice
-> -> -> xorg-libxft
-> -> -> gobject-introspection
-> -> leptonica
-> -> -> libtiff
-> -> -> -> libjpeg-turbo
-> log4cplus
```


## Notes

The example license plate photos stored in `./photos` are ranked from
"easy to read" to "hard to read".

The script (or actually, the `image_to_print` function) prints each license plate found in the specified photo.
For each plate it will print the possible strings, with a
confidence number attached. If the license plate is prefixed with `+`
it means it matches the Dutch license plate pattern, if this is
not the case then the license plate is prefixed with a `-`.

Here is the (current) output of each photo:

`1.jpg`:

```
Plate #1:
          Plate   Confidence
  +       37TVR1   94.660286
  +       37TYR1   82.577583
```

`2.jpg`:

```
```

`3.jpg`:

```
Plate #1:
          Plate   Confidence
  +       94NLD5   94.939178
  +       94NLDS   85.909142
  +       94NL05   83.461891
  -       94NL0S   74.431862
```

`4.jpg`:

```
Plate #1:
          Plate   Confidence
  +       22XXX4   89.798851
  -       Z2XXX4   85.786667
  -       2ZXXX4   81.732620
  -       ZZXXX4   77.720428
```

`5.jpg`:

```
```

`6.jpg`:

```
Plate #1:
          Plate   Confidence
  -        30RPB   88.336792
  -        3ORPB   85.447754
  +       30RPPB   83.388290
  -        3QRPB   81.638657
  -        3DRPB   81.547638
```


## Bugs

* ~~It doesn't seem to be able to read `2.jpg`, whilst this should
be pretty easy to do so since it's a clean, close-up picture.~~
(This seems to be caused by a setting in the config, specifically
`max_plate_{width,height}_percent`.)
It's also unable to read `5.jpg`, but that's a pretty crappy photo anyways.

* The `alpr.unload()` line causes this script to end with a
`SIGSEGV (Address boundary error)`.

* ~~It doesn't read out hyphens correctly 100% of the time~~ (now it is, using regex substitution).
See https://github.com/openalpr/openalpr/issues/416
