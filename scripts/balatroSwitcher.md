# :black_joker: Balatro Config Switcher :slot_machine:
A quick utility to change your Balatro mods/configs

## Usage
- Make sure that PowerShell 5+ is installed (I recommend 7+ to be sure, get it [here, the `-win-x64.msi`](https://github.com/PowerShell/PowerShell/releases/latest))
- Download the [script](https://raw.githubusercontent.com/EDM115/useful-stuff/refs/heads/main/scripts/balatroSwitcher.ps1) and save it in a convenient place
- [**:warning: CONFIGURE IT !!**](#Configuration)
- Open your PowerShell terminal (use Windows Terminal for instance and use the correct profile with the arrow next to the plus), and enter the path to the file (or just `./balatroSwitcher.ps1` if you're already in its directory)
- Type the number of the desired profile
- Enjoy !

## Configuration
- Step 0 : **BACKUP YOUR DATA !**  
  Save the content of `%APPDATA%\Balatro` somewhere else just in case something breaks because you misconfigured it.
- Step 1 : Prepare the folders  
  Copy the different versions/sets of mods you plan to use to a new directory in `%APPDATA%\Balatro` called `Switcher`. Make sure to give them distinct names.  
  With this, you can create a solo profile, a multiplayer, an experimental multiplayer (like here to play with more than 2 people), a heavily modded Cryptid profile... It's endless !
- Step 2 : Edit the script  
  Now that your files are ready, it's time to change the script :smiling_imp:  
  Yes it's tiresome but it works. No there is no GUI. *Embrace the CLI !*  
  
  The 3 default profiles will change the Steamodded, Multiplayer and JokerDisplay versions.  
  - If a version might change between profiles, include it in the respective `FoldersToDelete` array *(technical note : if an element takes only one line, no need for a comma separating the next one)*.  
    It's better to not have multiple versions of the same mod present !  
  - The `FoldersToCopy` array is straightforward : source to destination.  
    It's common for Steamodded to be called solely `smods`.  
  - The `FileEdits` array can be empty (`@()`) and is a special use-case.  
    It can be used to reconfigure mods (here disabling achievements in Multiplayer and re-enabling them in Solo, or switching profiles between a classic and a fully unlocked one).  
    It uses a regex to find the bit to replace and supports zlib compressed files (this will only concern `settings.jkr` and the files in the profiles (numbered folders).  
    Tip : To know what values to edit in these files, load them in https://balatro.shorty.systems/ and check the Raw tab.  
    Mod config files aren't compressed, check if you can read them in your notepad to make sure of this).  
  - If you need to create another profile, copy the existing structure (mention it in the list at the top, create the respective `FoldersToDelete`, `FoldersToCopy` and `FileEdits` variables, and add it in the switch case at the bottom with the corresponding number and params).
