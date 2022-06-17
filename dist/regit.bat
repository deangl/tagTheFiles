reg add "HKEY_CLASSES_ROOT\*\shell\tagthisfile" /ve /t REG_SZ /d "Tag This File" /f
reg add "HKEY_CLASSES_ROOT\*\shell\tagthisfile\command" /ve /t REG_SZ /d "%~dp0tagSetter.exe \"%%0\"" /f

