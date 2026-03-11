---
layout: post
title: "Link Error When Compiling and Installing Python Package in Windows"
date: 2016-02-23
categories: 
  - "corcpp"
  - "python"
---

It's usually easy to install a Python package in Windows with pip or other pre-built binaries. However, sometimes we must build the binary from source by ourselves, such as Basemap module, a part of matplotlib-toolkit.  
Then we may meet some error just like this:

```
Error c1010070: Failed to load and parse the manifest ...
```

Actually, there's a small bug in the "Distutils" component in some versions of Python. This bug has not been repaired until Dec. 2014 and has influence on Python 2.7, 3.4, 3.5. (See Reference: [Python Distutils Issue](https://bugs.python.org/issue4431))

When compiling and linking using MSVC toolchain, Python uses a MANIFEST file. However, Python doesn't pass /MANIFEST option to the linker so the linker will not generate the MANIFEST file correctly (See Reference: [Linker Options (VS2013)](https://msdn.microsoft.com/en-us/library/y0zzbyt4\(v=vs.120\).aspx))

The proper way is to pass /MANIFEST option to the linker by adding a line to manifest\_setup\_ldargs() in <python-install-prefix>/lib/distutils/msvc9compiler.py

```
    def manifest_setup_ldargs(self, output_filename, build_temp, ld_args):
        temp_manifest = os.path.join(
                build_temp,
                os.path.basename(output_filename) + ".manifest")
        ld_args.append('/MANIFESTFILE:' + temp_manifest)
        ld_args.append('/MANIFEST')
```

This bug might be solved in newer versions.
