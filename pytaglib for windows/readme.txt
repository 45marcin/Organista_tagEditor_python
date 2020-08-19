
    Install Microsoft Visual Studio 2015 Community Edition. In the installation process, be sure to enable C/C++ support.
    Download and build taglib:
        Download the current taglib release and extract it somewhere on your computer.
        Start the VS2015 x64 Native Tools Command Prompt. On Windows 8/10, it might not appear in your start menu, but you can find it here: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2015\Visual Studio Tools\Windows Desktop Command Prompts
        Navigate to the extracted taglib folder and type: cmake -G "Visual Studio 16 2019" -DCMAKE_INSTALL_PREFIX=".\taglib-install" to generate the Visual Studio project files.
        Type msbuild INSTALL.vcxproj /p:Configuration=Release which will "install" taglib into the taglib-install subdirectory.
    Still in the VS2015 command prompt, navigate to the pytaglib directory.
    Tell pytaglib where to find taglib: set TAGLIB_HOME=C:\Path\To\Taglib\taglib-install
    Build pytaglib: python setup.py build and install: python setup.py install
