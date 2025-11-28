@echo off
setlocal enabledelayedexpansion

:: Loop through each file with a pattern of *S??E??*
for %%F in (*S??E??.*) do (
    rem Extract just the filename
    set "filename=%%~nF"
    
    rem Use regex to find the SxxExx pattern
    echo !filename! | findstr /r /c:"S[0-9][0-9]E[0-9][0-9]" >nul && (
        
        rem Extract episode part and keep only Exx
        for /f "tokens=1,* delims=E" %%a in ("!filename!") do (
            set "episode=%%b"
        )
        for /f "tokens=1,* delims=." %%a in ("!episode!") do (
            set "newname=E%%a"
        )
        
        rem Rename file to Exx.ext
        if not "!filename!"=="!newname!" (
            echo Renaming "%%F" to "!newname!%%~xF"
            ren "%%F" "!newname!%%~xF"
        )
    )
)

pause
