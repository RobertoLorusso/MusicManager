from lxml import etree as ET
import numpy as np
import sys
import os
import subprocess
import shutil
import regex
import mdfind

""" 
This script takes the path of an XML file generated by Apple Music in order to check 
if the songs listed in the XML are already converted (present in the file system) and if so,
creates a folder named as the XML file (playlist name) in which are placed the links (or copies) 
to the original files.
Other operations are given.

NB: The path given for searching the songs MUST HAVE subfolders containing the following pattern: Artist/Album/Song 
    otherwise the songs will never be detected. 

========= EXAMPLE =========== 

Path: Users/username/Genres/

Where Genres contains folders structured in this way:
    Disco/ArtistName/AlbumName/SongName.mp3
    Jazz/ArtistName/AlbumName/SongName.mp3
    etc...

 ========= WARNING ===========
 
Sometimes it is necessary to check if the songs contained in a Genre folder have the same musical genre of it.
Example: R&B/Soul must contain only songs of that genre. It's possible to check the metadata with "mdfind"

mdsongs = mdfind.mdfind(["kMDMusicalGenre== 'R&B/Soul' && kMDItemKind == 'Audio MP3'", '-onlyin', '/Users/Roberto/Music/MacSoft'])
songs = regex.split('\n',mdsongs)

"""

# path = "/Volumes/MSDOS/Musica/1) Genres/R&B_Soul/"
# xml = "/Users/Roberto/Documents/R&B_Soul.xml"
# songs = "/Users/Roberto/Desktop/songs.xml"


# TODO The function AMXML.tolink() searches only for .mp3 extensions, make it more general with glob and wildcard *
# TODO The function AMXML.tolink() is linux dependent in the creations of links
# TODO use exceptions and logs to inform about the absence of a file in the File system, at the moment this is done in getmissing()


# BUG (Resolved): Description in AMXML.getsymbols()
# Method for resolving the bug:
# a = []
# for el in src.missing_songs:
#    a.append(dst.root.xpath('.//Artist[text()="'+el[0]+'"]/Album[text()="'+el[1]+'"]/Song[text()="'+el[2]+'"]'))


# BUG: when invoking tolink() the songs are misclaffied as 'Missing' and inserted into self.missing_songs errousnely
#       because they are missing in a genre BUT they are effectively presente in ANOTHER
#      A workaourond can be that of placing a song in missing_songs if a flag remains false after walking in all directories


class AMXML:
    def __init__(self, default=True):

        self.song_list = []  # List of lists, each list refers to a single song
        self.missing_songs = []
        if default == False:
            print("Path of XML generated by Apple Music")
            (path, b) = self.checkpath(type="f")
            if b:
                self.xml_path = path  # Path of the XML file
            print(
                "\nPath to directory in which search the files following the pattern Artist/Album/Song:"
            )
            (path, b) = self.checkpath()
            if b:
                self.path = path
        else:
            self.xml_path = "/Users/Roberto/Documents/R&B_Soul.xml"
            self.path = "/Volumes/MSDOS/Musica/1) Genres/"
        self.root = ET.XML(ET.tostring(ET.parse(self.xml_path)))

        self.tolist()

    def checkpath(self, type="d"):
        """
        Validate an input path.
        A type between 'd' (dir) and 'f' (file) can be specified
        """
        input_text = ""
        b = True
        ex = False
        while b:
            try:
                print("Input path or 'exit':")
                input_text = input()  # Read input
                if input_text == "exit":
                    b = False
                    sys.exit("Quitting...")
                if type == "d":
                    if os.path.isdir(
                        os.path.abspath(input_text)
                    ):  # Check if it's a dir
                        input_text = os.path.abspath(input_text)
                        return (input_text, True)
                    else:
                        print("\nNot a directory:" + str(input_text))
                        b = True  # continue to ask
                else:
                    if os.path.isfile(
                        os.path.abspath(input_text)
                    ):  # Check if it's a file
                        input_text = os.path.abspath(input_text)
                        return (input_text, True)
                    else:
                        print("\nNot a file:" + str(input_text))
                        b = True  # continue to ask

            except:
                print("\nBye!\n")

        if ex:
            exit(0)  # Exit without errors

    def tolist(self):
        """
        Extract informations about songs from Apple Music XML.
        """
        search = self.root.xpath(
            ".//dict/dict/dict"
        )  # Every song record has this pattern

        for i in range(0, len(search)):
            art = (
                search[i]
                .xpath('.//key[text()="Artist"]/following-sibling::string')[0]
                .text
            )
            alb = (
                search[i]
                .xpath('.//key[text()="Album"]/following-sibling::string')[0]
                .text
            )
            song = (
                search[i]
                .xpath('.//key[text()="Name"]/following-sibling::string')[0]
                .text
            )
            self.song_list.append([art, alb, song])  # Author, Album, Song

    def tolink(self, type="s"):
        """
        INPUT: type = "s" creates a symlink to the file, else copies it
        OUTPUT: folder containing the links/copies of songs specified in Apple Music XML
        """

        dst_path = os.path.join(
            self.path, os.path.splitext(
                os.path.basename(self.xml_path))[0] + "_link"
        )  # Folder in which place the links
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)

        # Mark all the songs as missing and remove them from the list if they are found
        self.missing_songs = []
        for i in range(0, len(self.song_list)):
            art = "".join(regex.split(
                '[:"/?]', self.song_list[i][0])).strip('"')
            alb = "".join(regex.split(
                '[:"/?]', self.song_list[i][1])).strip('"')
            song = "".join(regex.split(
                '[:"/?]', self.song_list[i][2])).strip('"')
            self.missing_songs.append([art, alb, song])

        # Get all the subfolders of self.path i.e. the musical genres
        subfolders = [dir for dir in os.listdir(
            self.path) if os.path.isdir(os.path.join(self.path, dir))]

        for genre in subfolders:

            for i in range(0, len(self.song_list)):

                # Check for the song at the path src_path/Author/Album/Song
                # bcs at the moment i'm converting the songs following this path convention
                # Remove the symbols removed by the converter i.e symbols which are present in the XML generated by Apple Music
                # and missing in the dirs and file names. These are inserted into regex.split function.
                art = "".join(regex.split(
                    '[:"/?]', self.song_list[i][0])).strip('"')
                alb = "".join(regex.split(
                    '[:"/?]', self.song_list[i][1])).strip('"')
                song = "".join(regex.split(
                    '[:"/?]', self.song_list[i][2])).strip('"')

                song_path = os.path.join(
                    self.path, genre, art, alb, song + ".mp3")

                if os.path.exists(song_path):  # and os.path.isfile(song_path):
                    try:
                        if type == "s":
                            # Shell call to symlink the file
                            subprocess.call(
                                "ln -s " + '"' + song_path + '"' + " " + '"' + dst_path + '"', shell=True)
                        elif type == "c":
                            shutil.copy2(song_path, dst_path)  # Make a copy

                        # remove from missing songs
                        self.missing_songs.remove([art, alb, song])

                    except Exception as e:
                        print("Exception raised in AMXML.tolink():")
                        print(e)

    def getmissing(self):
        """
        Get the Artists and their songs that are missing at AMXML.path
        """
        if len(self.missing_songs) == 0:
            # Don't create link or copies, just verify existence of the songs at self.path
            self.tolink(type=None)

        arts = []  # Artists in AMXML
        for i in range(0, len(self.missing_songs)):
            if self.missing_songs[i][0] not in arts:
                arts.append(self.missing_songs[i][0])

        arts = np.sort(arts)
        arts_songs = {}

        for el in arts:
            arts_songs[el] = []
            for i in range(0, len(self.missing_songs)):
                if (
                    self.missing_songs[i][0] == el
                ):  # If the song matches the artist insert the song into the list
                    arts_songs[el].append(
                        [self.missing_songs[i][1], self.missing_songs[i][2]]
                    )

        return arts, arts_songs

    def getsymbols(self):
        """
        This function takes as input the data returned by AMXML.getmissing() and returns
        the non-alphabetic symbols in their names.
        The purpose is to find the symbols which are present in the artists and songs names in the XML generated by Apple Music
        but missing in the stored dirs and file names.
        After a manual analysis of the symbols, if newly ones are detected, they have to be inserted into regex.split function
        into AMXML:getmissing(), otherwise the missing songs will contain tracks which are actually stored, but not recognized as
        they don't feature the symbols in their names.

        Pipeline: tolink() -> getmissing() -> getsymbols()
        """
        (
            arts,
            arts_songs,
        ) = self.getmissing()  # getmissing will call self.tolink(type=None)
        sym_arts = []
        for el in arts:
            symbols = ""
            for ele in arts_songs[el]:
                for element in ele:
                    symbols = symbols + \
                        "".join(regex.split("[A-Za-z]", element))
            sym_arts.append([symbols])

        # i = 0
        # for el in sym_arts:
        #    print((i, el))
        #    i = i + 1

        return sym_arts

    def findbygenre(self, op="==", genre="R&B/Soul", default=True):
        """
        This function takes as input a logical operator and the musical Genre and returns the result obtained by mdfind.
        The default parameter tells to the function to use the default path of the object, on which perform the search, or asks for another.
        """
        try:
            path = self.path
            if default == False:
                (path, b) = self.checkpath()

            # Search for .mp3 files with user option
            query = "kMDItemMusicalGenre " + op + " '" + \
                genre + "'" + " && kMDItemKind == 'Audio*' "
            mdsongs = mdfind.mdfind([query, "-onlyin", path])
            songs = regex.split("\n", mdsongs)  # Split on \n
            print("Found " + str(len(songs)) +
                  " songs that are " + op + " " + genre + " at path: " + path)
            return songs

        except Exception as e:
            print("\n\nException in AMXML.findByGenre():\n")
            print(e)
            print("\n\n")


#
# a = []
# for el in src.missing_songs:
#    a.append(
#        dst.xpath(
#            './/Artist[text()="'
#            + el[0]
#            + '"]/Album[text()="'
#            + el[1]
#            + '"]/Song[text()="'
#            + el[2]
#            + '"]'
#        )
#    )

# dst.xpath(".//Artist/Album/Song")
