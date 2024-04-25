## `sudo` on PowerShell

Microsoft plans on adding a sudo like command on windows ([info](https://winaero.com/linux-sudo-command-is-coming-to-windows-11/) and [controversy](https://winaero.com/microsofts-sudo-has-sparked-resentment-in-the-open-source-community/))  
But what if... you could already use it ? :hand_over_mouth:  
  
### Prerequisites

- Have the [newer version](https://github.com/PowerShell/PowerShell) of powershell installed.  
If you plan on using the old one, replace `pwsh` with `powershell`

### How ?

1. Open your powershell
2. Type `notepad $PROFILE` (can be another profile btw, more info [here](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.4#profile-types-and-locations))
3. Add the following :

```ps1
function sudo {
    # Create a command line string with properly escaped arguments
    $escapedArgs = @()
    foreach ($arg in $args) {
        if ($arg -match '\s') {
            # If argument contains spaces, wrap it in quotes and escape internal quotes
            $escapedArg = '"' + ($arg -replace '"', '\"') + '"'
        } else {
            # Just escape internal quotes
            $escapedArg = $arg -replace '"', '\"'
        }
        $escapedArgs += $escapedArg
    }
    
    $command = $escapedArgs -join ' '
    
    # Base64 encode the command to avoid PowerShell parsing
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($command + "; pause")
    $encodedCommand = [Convert]::ToBase64String($bytes)
    
    # Use Start-Process to execute the command in a new elevated PowerShell instance
    Start-Process pwsh -ArgumentList @("-ExecutionPolicy", "Bypass", "-EncodedCommand", $encodedCommand) -Verb RunAs
}
```

4. Reload your profile with `. $PROFILE`
  
Enjoy !

### Usage

```bash
sudo net start MySQL80

sudo tree /F "C:\idk\look a space\wow it handles quotes as well\and no need to wrap the command in quotes aswell\crazy"
```

If you want the elevated powershell to be reusable, add `"-NoExit"` at the start of the argument list.  
If you want the powershell to autoclose, delete ` + "; pause"` in the `$bytes` definition
