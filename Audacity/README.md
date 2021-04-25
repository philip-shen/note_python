Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Scripting - Audacity Development Manual - Audacity GUI](#scripting---audacity-development-manual---audacity-gui)
      * [Enable mod-script-pipe](#enable-mod-script-pipe)
   * [Scripting - Audacity Manual](#scripting---audacity-manual)
   * [Scripting Reference](#scripting-reference)
   * [Audacity Forum](#audacity-forum)
   * [audacity/scripts/piped-work/](#audacityscriptspiped-work)
   * [用於Mac的Python pywinauto for Audacity](#用於mac的python-pywinauto-for-audacity)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take note of Audacity Script  


# Scripting - Audacity Development Manual - Audacity GUI  
[Scripting - Audacity Development Manual - Audacity GUI 2021/3/8](https://alphamanual.audacityteam.org/index.php?title=Scripting&redirect=no)

## Enable mod-script-pipe  
```
The plug-in module "mod-script-pipe" is not enabled by default in Audacity, so must be enabled in Audacity preferences.

After enabling it for the first time, you will need to restart Audacity. You can then check that it is enabled and was started by revisiting the preferences page.

    Run Audacity
    Go into Edit > Preferences > Modules
        Choose mod-script-pipe (which should show New) and change that to Enabled. 
    Restart Audacity
    Check that it now does show Enabled.

This establishes that Audacity is finding mod-script pipe, and that the version is compatible. 
```


# Scripting - Audacity Manual  
[Scripting - Audacity Manual 2021/3/9](https://manual.audacityteam.org/man/scripting.html)


# Scripting Reference  
[Scripting Reference ](https://manual.audacityteam.org/man/scripting_reference.html)


# Audacity Forum  
[Audacity Forum](https://forum.audacityteam.org/)


# audacity/scripts/piped-work/   
[audacity/scripts/piped-work/](https://github.com/audacity/audacity/tree/master/scripts/piped-work)
```
=piped-work folder=

This folder contains scripts for exercising mod-script-pipe

To run a simple test to check communications:
   python pipe_test.py
or:
   python3 pipe_test.py

A much longer test that produces many image.
This script requires files from the "tests/samples/" folder and writes images
to "/tests/results/" folder, both of which are in the root of the source tree.
   python docimages_all.py
```


# 用於Mac的Python pywinauto for Audacity 
[用於Mac的Python pywinauto for Audacity 2017-04-12](http://hk.uwenku.com/question/p-gfmqbdpy-ss.html)
```
import pywinauto 
from pywinauto import application 

def noiseReduce(filename): 
    app = application.Application() 
    app = app.connect(path=r'/Applications/Audacity') 
    app.captcha20170411_202241.menu_select('File->Import->Audio') 
    app.Selectoneormoreaudiofiles.Edit.SetText(filename + '.wav') 
```

# Troubleshooting


# Reference


* []()
![alt tag]()
<img src="" width="400" height="500">

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3




