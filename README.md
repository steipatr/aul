# aul

Export [NetLogo](https://ccl.northwestern.edu/netlogo/) simulation runs as GIF or MP4 using Python.

## Purpose
The purpose of this project is to provide a simple and reliable way of capturing/exporting NetLogo simulation runs in moving image file formats.
Currently, MP4 and GIF are supported. These formats are suitable for sharing on social media or instant messager, or embedding in presentations or
documents.

## Installation

This library was tested on Python 3.6+. Requirements are:
* [pyNetLogo](http://pynetlogo.readthedocs.io/en/latest/)
* [imageio](http://imageio.github.io/)
* [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) (if you want MP4 export)

These packages also have their own requirements, especially [pyNetLogo's jpype dependency](https://pynetlogo.readthedocs.io/en/latest/install.html).

Install using:

```
$ pip install aul
```

## Usage

The two main functions in the package are `export_gif()` and `export_mp4()`. Both can take a variety of arguments, but also have useful default behavior. 
Two parameters are required: the NetLogo model name (must be in same folder as Python file), and the ticks to be exported.

### Basics

Export first 30 ticks of simulation run to GIF...

```py
import aul

#ticks 0 to 24
aul.export_gif('Fire.nlogo',30)

```

or MP4.

```py
import aul

#first 30 
aul.export_mp4('Fire.nlogo',30)

```

### Ticks

You can specify ticks in three ways - as an integer (see above), or a two- or three-parameter list:

```py
import aul

#ticks 0 to 24
aul.export_gif('Fire.nlogo',[0,25])

```

if you don't want every tick:

```py
import aul

#every tenth tick up to 200
aul.export_mp4('Fire.nlogo',[0,200,10])

```

### General Arguments
Simulation runs will normally be performed with the input parameter (slider, switch, chooser, etc.) values saved in the NetLogo model.
You can override these values directly from Python by passing a dictionary of values to `params`:

```py
import aul

fire_params = {
    "density":90,
    "probability-of-spread":60
}

aul.export_gif('Fire Simple Extension 1.nlogo',45,params=fire_params)

```

By default, the generated file will have the same pixel dimensions as the NetLogo world. You can adjust this with `scale`:

```py
import aul

#GIF file will be twice as large as NetLogo world
aul.export_gif('Fire Simple Extension 1.nlogo', 45, scale = 2.0)

```

You can also fade the last few frames of the run to black to emphasize it is terminating with `fade`:

```py
import aul

#GIF will fade to black over last 30% of runtime
aul.export_gif('Fire Simple Extension 1.nlogo', 45, fade = 0.3)

```

You can set the name of the output file with `name`.

```py
import aul

#GIF will be saved as "custom-fire.gif"
aul.export_gif('Fire Simple Extension 1.nlogo', 45, name = "custom-fire")

```

Per NetLogo conventions, the initialization and iteration procedures are expected to be named *setup* and *go*. Override these
defaults with the `setup` and `go` parameters. Adjust the playback speed of the output file with `fps` (frames per second).


### GIF-specific Arguments

You can optimize GIF storage by settings `subrectangles = True`.

### MP4-specific Arguments

You can optimize MP4 storage with the `quality` argument. Default is max quality (and thus max file size).
