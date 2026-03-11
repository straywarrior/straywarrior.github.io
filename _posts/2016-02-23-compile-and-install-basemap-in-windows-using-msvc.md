---
layout: post
title: "Compile and Install Basemap in Windows (Using MSVC)"
date: 2016-02-23
categories: 
  - "python"
  - "mswindows"
---

Basemap is a Python package, which never releases new update after 2014. It's easy to use in Linux or OS X but not easy to install on Windows. It doesn't supply setup-package for Python 3.4 or 3.5 or newer version. For Python 2.6/2.7/3.2/3.3, there're pre-built setup-package which are easy to use. (See [SourceForge.net](https://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/)) However, if we want to use Python 3.4 or higher version, it seems to be necessary for us to compile it by ourselves.

It's a guide about compiling and installing basemap in Windows using Microsoft C/C++ compiler.

### Pre-Requirements

CMake (See [CMake](https://cmake.org/)) Microsoft C/C++ Compiler (See [Microsoft Visual Studio](https://www.visualstudio.com/en-us/downloads/download-visual-studio-vs.aspx)) Python 3.4 or later (See [Python](https://www.python.org/)) Matplotlib (See [Matplotlib](https://sourceforge.net/projects/matplotlib/files/matplotlib/))

### Build All Dependencies and Basemap

#### Build GEOS

Download geos-3.5.0.tar.gz (See [GEOS](https://trac.osgeo.org/geos/)) _NOTE: The geos shipped with basemap is geos-3.3.0 but there are some small bugs in version 3.3.0 which cause compiling error with MSVC. So we use the newest version instead. The API provided in version 3.5.0 is the same as that in version 3.3.0_

Extract source files to a directory such as E:\\Temp\\geos-3.5.0 Create a new directory for building such as E:\\Temp\\geos-3.5.0\\build

**Important:** A required file is missed from the source tarball for some reason that I don't know. I put it in the Appendix. Copy and save it to E:\\Temp\\geos-3.5.0\\cmake\\modules\\GenerateSourceGroups.cmake

Run CMake-Gui and specify the source directory and build directory and click **Configure**. Modify the **CMAKE\_INSTALL\_PREFIX** to where you like, such as E:/geos  (use slash in path). Then click **Generate** and Visual Studio Solution files should be generated in the build directory (E:\\Temp\\goes-3.5.0 in this case).

Open the **geos.sln** using Visual Studio. Change the build-type to 'Release' and generate the project **ALL\_BUILD** After building all sources, generate the project **INSTALL** and then the headers, static libraries (\*.lib) and dynamic libraries (\*.dll) will be installed to CMAKE\_INSTALL\_PREFIX (E:\\goes in this case).

#### Build Basemap

Download basemap-1.0.7.tar.gz (See [SourceForge.net](https://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/)) Extract source files to a directory such as E:\\Temp\\basemap-1.0.7

##### Pre-build Preparation

\* Check your Python's distutils component to make sure the msvc9compiler.py is correct. (See Reference [Link Error When Compiling and Installing Python Package in Windows](/posts/link-error-when-compiling-and-installing-python-package-in-windows) \* Find the Line 79 of basemap-1.0.7\\setup.py . Make sure that geos\_c  is in libraries  (It's missed in basemap-1.0.7 and you will meet Link Error when building \_geoslib).

```
    extensions.append(Extension("_geoslib",['src/_geoslib.c'],
                                library_dirs=geos_library_dirs,
                                include_dirs=geos_include_dirs,
                                libraries=['geos_c', 'geos']))
```

##### Build and Install

Run **VS2013 x86 Native Tools Command Prompt** (which can be found in Visual Studio Tools in Startup Menu), or **VS2013 x64 Native Tools Command Prompt** if you use 64-bit Python. (To tell which architecture of Python you are using, run python in command line and you will find it) Go into the basemap directory and set proper environment variable GEOS\_DIR :

```
cd /D E:\Temp\basemap-1.0.7
set GEOS_DIR=E:\geos
```

_Note: Do not add quotation marks (") to the path even if there are spaces like "Program Files"._ Python always tries to find some specific version of MSVC(using Environment Variable such as VS100COMNTOOLS) and raise Error "Unable to find vcvarsall.bat". So we need to set proper environment that points to MSVC 2013:

```
SET VS100COMNTOOLS=%VS120COMNTOOLS%
```

Then we can build and install the basemap package:

```
python setup.py install
```

If there is no error, congratulations.

#### The Final Step

Run python from command line and let's check whether Basemap is working:

```
from mpl_toolkits.basemap import Basemap
```

You may find that there's a strange error:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<python-install-prefix>\lib\site-packages\mpl_toolkits\basemap
.py", line 37, in <module>
    import _geoslib
ImportError: DLL load failed: The specified module could not be found.
```

You can find **\_geoslib.pyd** in **<python-install-prefix>\\lib\\site-packages** But if you check the dependencies of \_geoslib.pyd you will find that it needs **geos\_c.dll**, which is not in search path of dynamic libraries (E:\\geos\\bin in this case). There are two ways to solve this problem: \* Add the geos\_c.dll path to your environment variable PATH. \* Or copy geos\_c.dll and geos.dll to <python-install-prefix>\\lib\\site-packages

Now, basemap is installed properly. Enjoy using it in your codes :)

### Appendix

#### GenerateSourceGroups.cmake

```
#
# Macro generates tree of IDE source groups based on folders structure
# Source: http://www.cmake.org/pipermail/cmake/2013-November/056332.html
# 
macro(GenerateSourceGroups curdir)
  file(GLOB children RELATIVE ${PROJECT_SOURCE_DIR}/${curdir} ${PROJECT_SOURCE_DIR}/${curdir}/*)
  foreach(child ${children})
    if(IS_DIRECTORY ${PROJECT_SOURCE_DIR}/${curdir}/${child})
      GenerateSourceGroups(${curdir}/${child})
    else()
      string(REPLACE "/" "\\" groupname ${curdir})
      # I would like to call the src root folder in a different name, only in visual studio (not mandatory requirement)
	  string(REPLACE "src" "Source Files" groupname ${groupname})
      source_group(${groupname} FILES ${PROJECT_SOURCE_DIR}/${curdir}/${child})
    endif()
  endforeach()
endmacro()
```
