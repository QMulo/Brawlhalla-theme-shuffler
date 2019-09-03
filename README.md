# Brawlhalla-theme-shuffler

Shuffle between [Brawlhalla](http://www.brawlhalla.com/) map themes/assets quickly.

BMG devs have gone out of their way to make modding stages, the UI, and the in-game music as simple as possible. Nearly all stage assets are stored as simple, editable images files (png, jpg), with stage music stored as mp3 files.

In addition to the stages, nearly all UI elements are customizable - this includes stage backgrounds, buttons, borders, and even the daily rotating "tiles" on the landing page.

This script allows you to quickly shuffle between sets of map textures and other assets.

## Quickstart (Windows)

Install [python](https://www.python.org/downloads/)

Clone this repo (or download/unzip)

Double-click `batch_scripts/brawlhalla_shuffle.bat`

Load Brawlhalla.

If the script worked properly, your background should now feature Ada, and a few tiles will have additional captions.

Now, start a Training match on Enigma.

The stage should now be made of either pink/purple crystals or greek columns.

Now, exit Brawlhalla. Change the name of `examples/UI/force - My Custom UI` to `examples/UI/disable - My Custom UI`. 

Double-click `batch_scripts/brawlhalla_shuffle.bat`

Load Brawlhalla.

If the script worked properly, your background should now feature either Diana or Koji, and the tile will all be returned to normal.


## Setup/Installation Instructions

Install [python](https://www.python.org/downloads/)

Clone this repo (or download/unzip)

Edit `config.json` as necessary:

   `brawlhalla_home` - directory where Brawlhalla is located (will also try default Steam install directories)

   `allow_defaults` - include the default map textures/assets as an option when randomly selecting a theme. By default, the original assets will not be used if there is at least one alternative are available. 

   `asset_dir` - where your custom themes are stored (and where backups of the original assets will be stored). 

   `reset_before_shuffle` - if `true`, original assets will be restored before selecting a new theme. Useful in cases where certain themes overwrite files that others don't (eg, if you selected a theme which edits the map thumbnail, then later selected a theme for the same map that does not edit the thumbnail, you would still see the thumbnail from the first map)


## Folders and Files

All file/folder names are case-sensitive

Do not name any skin folders "default" (these will be autogenerated by the script)

All folders/subfolders/files are optional. For example, not every skin/theme has mp3 files, or you may not want to alter thumbnail images.

### Directory Structure - Shuffle per-map

It is recommended to have one directory per-map. However, if you want to create additional folders, you will need to update `config.json` (see next section on folder names).

Assets in `asset_dir` must be stored in the following structure (see "examples" folder)

```
  - {Map Name}
    - {Skin Name}
        - mapArt
          - Backgrounds
          - {Map Name}
        - images
          - thumbnails
          - ...
        - mp3
```

### Alternate Directory Structure - Shuffle Multi-map themes

If you want to shuffle between themes that span multiple maps, such as [Mook_Mook's Afternoon Edits](https://gamebanana.com/maps/204413) or [saintijames99's 80s Maps Pack](https://gamebanana.com/maps/202608), you can place them in the same folder. You will need to ensure to update `included_maps` in `config.json` with whatever you name the top-level folder (in this case, "MasterThemes").

You may also want to set `reset_before_shuffle` to `true`, which will ensure any files not overwritten by the new theme are reverted to the original asset. 

```
  - MasterThemes
    - Mook's Afternoon Edits
        - mapArt
          - Backgrounds
          - BattleHill
          - Brawlhaven
          - ...
        - images
          - thumbnails
          - ...
        - mp3
    - 80s Theme
        - mapArt
          - Backgrounds
          - BattleHill
          - Brawlhaven
          - ...
        - images
          - thumbnails
          - ...
        - mp3
```

### Notes on folder names

Blacklist: Prefix a skin name with "disable" to disable the skin as an option (eg, "disable - My Brawlhaven Theme"). This is great for when you have one or two joke maps or WIP maps you want to temporarily disable

Whitelist: If any skin names in a folder start with "force", the script will only choose skins from those folders. Great if you want to try out a single new map, or if you have a large number of options and want to narrow it down to 1-or-2.

If `included_folders` is configured, the script will only look in those folders, and in the order they are listed. Otherwise, the script will look in every folder in `asset_dir` that is not in `excluded_folders`.

For example, in the `examples` folder, there are custom assets stored in `UI/My Custom UI`, and `UI` has been added to the `included_maps` section of the config file.


## Using the script

The `batch_scripts/` directory includes batch scripts for shortcuts/double-click/macros convenience on Windows

Start the script using one of these methods:
- Double-click: `batch_scripts/brawlhalla_shuffle.bat` 
- Command line: `python brawlhalla_shuffle.py`

The script will perform the following:

- Read `config.json`
- Find every directory in the `included_maps`  `asset_dir`
- For each folder within `asset_dir`, determine what skins are available, and select one at random
- If `reset_before_shuffle` is set to `true`, revert any files that have been overwritten to the original asset 
- Find all files within that skin folder that also exist in the Brawlhalla asset directory. 
- For each of those files:
  - If the file has not been backed up, create a copy of the original file in the `default` skin folder
  - Overwrite the file in the Brawlhalla directory with the skin's file
  - Any files in the skin folder that do not exist in the Brawlhalla home assets will not be copied 

### When changes take effect

Map assets are loaded at the beginning of each match. You can run the script during or between matches, and the new maps will be loaded before your next match. Your changes will not be shown with in a match - however, if you leave, load a new theme, then rejoin a match, your changes will show.

UI assets, however, are loaded at the start of the game. You will have to exit and restart if you want to change UI elements, including map thumbnails.

### Reset to Original Files

#### Using Steam

Right click on the game in steam, navigating to Properties > Local Files > Verify Integrity of Game Files. Steam will detect that your local files have been altered and will redownload/overwrite them with the official assets

#### Using the script

Run `python brawlhalla_shuffle.py -r`, or start `batch_scripts/reset_to_default.bat`

## Where to get themes

The easiest place to get started [brawlhallamods.blogspot.com](https://brawlhallamods.blogspot.com/) by [lmiol](https://steamcommunity.com/sharedfiles/filedetails/?id=1220997335) - he all of the maps consistently organized, and his FAQ is the simplest way to manually import modded maps 

Additional themes available at [gamebanana](https://gamebanana.com/maps/games/5704).