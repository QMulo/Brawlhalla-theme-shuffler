import os
import shutil
import random
import argparse
import json


DEFAULT_STEAM_32_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Brawlhalla"
DEFAULT_STEAM_64_PATH = "C:/Program Files/Steam/steamapps/common/Brawlhalla"


def read_config():
    os.chdir(os.path.dirname(__file__))
    script_dir = os.path.abspath(os.path.dirname(__file__))
    json_filename = os.path.join(script_dir, "config.json")
    with open(json_filename) as f_in:
        json_data = json.loads(f_in.read())
    return json_data


class BrawlhallaShuffler:
    def __init__(self):
        """
        Initialize shuffler and set config"
        """
        self.config = read_config()
        self.asset_dir = os.path.abspath(os.path.expanduser(self.config["asset_dir"]))

        self.default_dir = self.config.get("brawlhalla_home")
        self.allow_defaults = self.config.get("allow_defaults", False)
        self.reset_before_shuffle = self.config.get("reset_before_shuffle", True)

        self.included_maps = self.config.get("included_maps", [])
        self.excluded_maps = self.config.get("excluded_maps", [])
        self.sync_folders = self.config.get("sync_folders", [
            "images/thumbnails",
            "images/chests",
            "images/tiles",
            "images/UI",
            "mapArt/Backgrounds",
            "mapArt/{map_name}",
            "mp3",
        ])

        if not self.default_dir or not os.path.exists(self.default_dir):
            if os.path.exists(DEFAULT_STEAM_32_PATH):
                self.default_dir = DEFAULT_STEAM_32_PATH
            elif os.path.exists(DEFAULT_STEAM_64_PATH):
                self.default_dir = DEFAULT_STEAM_64_PATH
            else:
                raise ValueError("Cannot locate `brawlhalla_home` directory in config")

    def map_choices(self):
        """
        Returns list of maps with at least 1 non-default, non-disabled option
        """
        available_maps = [
            x for x in os.listdir(self.asset_dir) if x not in (
                "default",
                "defaults",
                "Backgrounds",
            ) 
            and os.path.isdir(os.path.join(self.asset_dir, x))
            and len(self.skin_choices(x)) > 0
            and x not in self.excluded_maps
        ]
        if self.included_maps and len(self.included_maps) > 0:
            available_maps = [x for x in self.included_maps if x in available_maps]
        return available_maps

    def skin_choices(self, map_name):
        """
        Returns list of non-disabled options for a map
        """

        # Filter out default (unless allowed); filter out disabled
        available_choices = [
            x for x in os.listdir(os.path.join(self.asset_dir, map_name)) if 
            os.path.isdir(os.path.join(self.asset_dir, map_name, x))
            and (self.allow_defaults or not x == "default") 
            and not x.lower().startswith("disable")
        ]

        # Whitelist
        # if any start with "force", keep only those
        force_choices = [
            x for x in available_choices if x.lower().startswith("force")
        ]
        if len(force_choices) > 0:
            return force_choices

        return available_choices

    def select_skin(self, map_name, allow_default=False):
        """Select a random option for a given map"""
        return random.choice(self.skin_choices(map_name))

    def backup_default(self, map_name, subfolder, file):
        """
        If this is the first time overwriting the file, create a default backup
        """
        default_file = os.path.join(self.asset_dir, map_name, "default", subfolder, file)
        old_asset = os.path.join(self.default_dir, subfolder, file)

        def ensure_folder(file_full):
            if not os.path.exists(os.path.dirname(file_full)):
                ensure_folder(os.path.dirname(file_full))
                os.mkdir(os.path.dirname(file_full))

        if not os.path.exists(default_file):
            ensure_folder(default_file)
            print("    - backing up {0}".format(os.path.join(map_name, subfolder, file)))
            backup_file = shutil.copy(old_asset, default_file)

    def copy_assets(self, theme_dir, skin):
        """
        Copy assets from map skin dir to Brawlhalla default asset dir
        """
        skin_dir = os.path.join(self.asset_dir, theme_dir, skin)

        output = []
        sync_folders = self.sync_folders.copy()

        if "mapArt/{map_name}" in sync_folders and os.path.exists(os.path.join(skin_dir, "mapArt")):
            for map_name in os.listdir(os.path.join(skin_dir, "mapArt")):
                if map_name != "Backgrounds":
                    sync_folders.append(os.path.join("mapArt", map_name))

        for folder_name in sync_folders:
            skin_subfolder = os.path.join(skin_dir, folder_name)

            # Skip if folder not present
            if not os.path.exists(skin_subfolder):
                continue
            skin_assets = os.listdir(skin_subfolder)

            for skin_file in skin_assets:
                new_asset = os.path.join(skin_subfolder, skin_file)
                old_asset = os.path.join(self.default_dir, folder_name, skin_file)
                if os.path.exists(old_asset):
                    if skin != "default":
                        self.backup_default(theme_dir, folder_name, skin_file)   
                    output.append(shutil.copy(new_asset, old_asset))
        print("    - {0} overwritten; {1} files".format(theme_dir, len(output)))

    def shuffle_assets(self, reset):
        """
        Main method for shuffling or resetting all assets
        """
        print("Shuffle Brawlhalla Themes")
        map_choices = self.map_choices()

        if reset or self.reset_before_shuffle:
            print("")
            print("  Resetting maps to default")
            for map_name in map_choices:
                self.reset_default(map_name)

        if not reset:
            print("")
            for map_name in map_choices:
                print(map_name)
                skin_choice = self.select_skin(map_name)
                print("  " + skin_choice)
                self.copy_assets(map_name, skin_choice)

    def reset_default(self, map_name):
        """
        Reset all assets to original from backup defaults
        """
        print("  Resetting: {0}".format(map_name))
        return self.copy_assets(map_name, "default")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shuffle Brawlhalla Assets')
    parser.add_argument('-d', action="store_true", default=False)
    parser.add_argument('-r', action="store_true", default=False)
    args = parser.parse_args()

    bh_shuffler = BrawlhallaShuffler()
    if args.d:
        bh_shuffler.allow_defaults = True
    bh_shuffler.shuffle_assets(reset=args.r)
