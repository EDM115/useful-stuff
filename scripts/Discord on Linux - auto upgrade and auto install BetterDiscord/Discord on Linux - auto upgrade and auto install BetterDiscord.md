## Discord on Linux : auto upgrade and auto install BetterDiscord

If you've installed discord on Linux through apt, you know how much of a pain it is to manually download and install it every now and then. It's even worse if you're having to reinstall BetterDiscord every time  
So here's 2 simple scripts to fix this : 

### `launch-discord.sh`

- Versatile script to launch discord
- Auto launches the upgrade script if needed (have to be in the same folder)
- Detaches the Discord instance from the terminal once done

> [!NOTE]  
> requires to use `sudo` when an upgrade is needed. In such case, needs the user param to be passed

> [!IMPORTANT]  
> Edit the path to the upgrade script on line 60 to an absolute path, this way you can run the command from any directory

**Usage :**

```bash
./launch-discord.sh -b BUILD -bd BOOL -u USER
```

- `-b` or `--build` : the build you have installed. can be `stable`, `ptb` or `canary`
- `-bd` or `--betterdiscord` : precise if you have BetterDiscord installed. can be `true` or anything else for `false`. can be ommited
- `-u` or `--user` : specify the user that will be used to run Discord, which can't be ran as root, so simply running the script as sudo will break things, this is why this param is needed

Example : `./launch-discord.sh -b ptb -bd true -u $(whoami)`

### `upgrade-discord.sh`

- Super simple script to upgrade Discord
- Automatically fetches the latest version if none is passed
- Launches Discord and lets it finishing to download its updates before installing BetterDiscord

**Usage :**

```bash
sudo ./upgrade-discord.sh -b BUILD -v VER -bd BOOL -u USER
```

- `sudo` : Because further commands requires sudo
- `-b` or `--build` : the build you have installed. can be `stable`, `ptb` or `canary`
- `-v` or `--version` : the version to download. if this script is run through `launch-discord.sh`, it will be the one that discord requests. format : `x.x.xx(x)`, when I'm writing this the versions are 0.0.50 for stable, 0.0.80 for ptb and 0.0.357 for canary. if not provided, downloads the latest version available
- `-bd` or `--betterdiscord` : precise if you have BetterDiscord installed. can be `true` or anything else for `false`. can be ommited
- `-u` or `--user` : specify the user that will be used to run Discord, which can't be ran as root, so simply running the script as sudo will break things, this is why this param is needed

Example : `sudo ./upgrade-discord.sh -b ptb -v 0.0.80 -bd true -u $(whoami)`

### `better-discord.desktop`

- A simple file so you can have on your desktop, app menu or dash the correct version

**Usage :**

```bash
sudo nano /usr/share/applications/better-discord.desktop
```

Copy-paste the content

> [!IMPORTANT]  
> Edit the path to the launch script (absolute path), and customize the arguments. Here the user have to be hardcoded

### Prerequisites

- Having wget and apt-get on your machine
- For BetterDiscord : having it installed through [betterdiscordctl](https://github.com/bb010g/betterdiscordctl)
- Allow the scripts to be executable (`chmod +x launch-discord.sh upgrade-discord.sh`)

### Notes

This may or may not work in the future, depending of how discord logs things when starting
