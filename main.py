"""
    A simple script to loop through a directory of Looney Tunes episodes and organizes them
    in a format that Plex can read. Thus far Seasons from 1929 to 1980 are supplied.

    The program requires the name to be at the end of the file name after a ( - ).
    EX: Some_Looney_Tunes_episode_named - Mucho Locos.mp4
    The episode name will be matched with Mucho Locos, capitalization does not matter, they will all be
    matched lowercase.

    There are various naming conventions and this program uses www.thetvdb.com
    naming. Some punctuation is different and may have to be manually altered inorder
    for the sorter to work.
    EX: Rabbit Stew and Rabbits Too!, Zip Zip Horray!, Ready.. Set.. Zoom!
    This punctuation needs to be correct, some naming conventions have slight variances

    I was unable to get non english characters to be seen as in the episode:
    Señorella and the Glass Huarache
    the ñ was replaced with n
    Characters such as : ½ were removed from episodes like: The Fighting 69½th, and
    Duck Dodgers and the Return of the 24 ½th Century,

    There was at least one : in one episode title and it is an illegal character for
    a file name, that was removed in the list.
"""

import os
import shutil
import episodes

__author__ = "Jeremy Lysinger"

__maintainer__ = "Jeremy Lysinger"
__email__ = "jeremy.lysinger@gmail.com"
__status__ = "Production"

new_path = "Desination folder of sorted episodes "
path = "Location of unsorted Episodes"
exclude = [".DS_Store"]  # excludes a file in macOS file system


def create_folder_move(save, season_idx, unsorted_path, episode_idx, ext, old_file_name):
    """
        creates a folder for each season in the form of Season 1929 if episode exists in season,
        if folder has already been created the file is moved to corresponding season folder
        Does not create root Looney Tunes folder
    """

    current_directory = os.path.join(save, episodes.library[season_idx][0])
    new_name = os.path.join(current_directory, episodes.library[season_idx][episode_idx])
    if os.path.isdir(current_directory):
        shutil.move(unsorted_path, current_directory)
        old_file = os.path.join(current_directory, old_file_name)
        os.rename(old_file, new_name + ext)
    else:
        os.makedirs(current_directory)
        shutil.move(unsorted_path, current_directory)
        old_file = os.path.join(current_directory, old_file_name)
        os.rename(old_file, new_name + ext)


def episode_maker(season_episode_list):
    """
    Removes Season and Episode numbers from beginning of each episode
    to match with unorganized episodes
    """

    episodes_only = []
    for episode in season_episode_list:
        episodes_only.append(episode[11:].lower())  # Makes lowercase for easier match
    return episodes_only


if __name__ == '__main__':
    for season in episodes.library:
        season_index = episodes.library.index(season)  # Season index position
        current_season = episode_maker(season)  #

        for dir, folders, files in os.walk(path):
            for file in sorted(files):
                if file not in exclude:
                    if file.partition(" - ")[2][:-4].lower() in current_season:  # Makes file lower case to match
                        extension = os.path.splitext(file)[1]
                        episode_index = current_season.index(file.partition(" - ")[2][:-4])
                        episode_path = os.path.join(dir, file)
                        create_folder_move(new_path, season_index, episode_path, episode_index, extension, file)
