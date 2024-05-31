"""A simple cx_Freeze setup script template.

How to use this script:
  1) add this file to your project directory
  2) install cx_Freeze ("python -m pip install cx_Freeze" via bash/terminal/powershell)
  3) fill out the 'BUILD SCRIP SETUP' section below
  4) invoke the script from bash/terminal/powershell via "python setup.py build"
"""
__version__      = "0.1.0"
__author__       = "Anthony Doupe"
__author_email__ = "anthony.doupe@microchip.com"


from typing import TypedDict, Sequence, Literal
from cx_Freeze import setup as _setup, Executable


class MetaData(TypedDict):
    name            : str  # [REQUIRED]: project or application name
    version         : str  # [REQUIRED]: version number of project, application, or executable as
                           #             'major.minor.patch' (ex. "0.1", "1.5.36")
    author          : str | None
    author_email    : str | None
    maintainer      : str | None
    url             : str | None
    description     : str | None
    long_description: str | None
    download_url    : str | None
    classifiers     : Sequence[str] | None
    platforms       : Sequence[str] | None
    keywords        : Sequence[str] | None
    license         : str | None


class BuildOpts(TypedDict):
    build_exe           : str | None               # defaults to ".//build//exe.[platform identifier].[python version]"
    optimize            : Literal[0, 1, 2] | None  # optimization level -- 0 == "disabled", 2 can brick app execution
                                                   # (make sure the .exe runs with 0 first before using the other options)
    # NOTE: cx_Freeze will *try* to follow imports of code used by the target script,
    #       so manually including modules is not always necessary.
    excludes            : Sequence[str] | None     # list of module names to exclude -- usually unnecessary since
                                                   # cx_Freeze won't include modules unless they are used by the
                                                   # target script
    includes            : Sequence[str] | None     # list of module names to include -- usually unnecessary unless
                                                   # cx_Freeze can't "find" them (i.e. the app uses dynamically imported code)
    packages            : Sequence[str] | None     # list of package names to include, i.e. all modules/sub-packages in
                                                   # the namespace (XXX for your sanity, always incl all third-party packages
                                                   # this way)
    include_files       : Sequence[str] | None     # list of paths pointing to other files/folders to include in the generated
                                                   # executable's directory
    include_msvcr       : bool | None              # `True` auto-includes `vcruntime.dll` from "C://Windows//System32"
                                                   # (XXX: this is "optional", which is nuts -- set to `True`)

    # These are more advanced and niche options. You won't need them often (if ever).
    replace_paths       : Sequence[str] | None
    path                : Sequence[str] | None
    no_compress         : bool | None
    constants           : str | None
    bin_includes        : Sequence[str] | None
    bin_excludes        : Sequence[str] | None
    bin_path_includes   : Sequence[str] | None
    bin_path_excludes   : Sequence[str] | None
    zip_includes        : Sequence[str] | None
    zip_include_packages: Sequence[str] | None
    zip_exclude_packages: Sequence[str] | None
    silent              : str | None
    silent_level        : str | None



def setup(metadata: MetaData, build_options: BuildOpts, *exec_options: Executable):
    return _setup(**metadata, options={"build_exe": build_options}, executables=exec_options)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BUILD SCRIPT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

METADATA = MetaData(
    name='scope_setup_v2.0',
    version='0.1',
)

BUILD_OPTS = BuildOpts(
    packages=['tkinter', 'tkintertable', 'pyvisa', 'pyvisa_py', 'numpy', 'psutil', 'zeroconf', 'pathlib'],
    includes=[],
    include_files=['commands.json'],
    include_msvcr=True,
    optimize=0,
)

EXEC_OPTS: Sequence[Executable] = [
    Executable(
        # script [REQUIRED]: name of top-level module/script (must incl `.py`)
        script='main_gui.py',

        # icon: filepath to a '.ico' file to use as the executable icon
        icon=None,

        # base: should be "Win32GUI" for win32 ui applications (which hides the main
        #       console), otherwise "console" or `None`
        base=None,

        # target_name: filename of created executable (must incl '.exe') -- defaults
        #              to *script* name
        target_name='scope_setup_v2.0',

        # XXX: There are others -- only the most useful are listed.
    ),
]





if __name__ == '__main__':
    setup(METADATA, BUILD_OPTS, *EXEC_OPTS)
