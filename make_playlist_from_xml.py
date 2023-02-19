from lxml import etree as ET
import numpy as np
import sys
import os
import subprocess
import shutil
import regex

# path = "/Volumes/MSDOS/Musica/1) Genres/R&B_Soul/"
# xml = "/Users/Roberto/Documents/R&B_Soul.xml"
# songs = "/Users/Roberto/Desktop/songs.xml"

""" This script takes the path of an XML file generated by Apple Music in order to check 
if the songs listed in the XML are already converted (present in the file system) and if so,
creates a folder named as the XML file (playlist name) in which are placed the links (or copies) 
to the original files"""

# TO-DO The function AMXML.tolink() searches only for .mp3 extensions, make it more general with glob and wildcard *
# TO-DO Make the function AMXML.tolink() search for songs in multiple folders instead of a single one
# TO-DO The function AMXML.tolink() is linux dependent in the creations of links
# TO-DO use exceptions and logs to inform about the absence of a file in the File system


# bug: in song_list vengono aggiunte le virgolette per alcuni record: Esempio [Childish Gambino, "Awaken, My Love!",...]
#  e quindi il path non risulta valido

# Questo ha risolto solo parte del problema, da 1225 sono scese a 1094

# missing_songs records 110 e 51 il metodo strip non funziona sempre

# Problema identificato così:

# a = []
# for el in src.missing_songs:
#    a.append(dst.root.xpath('.//Artist[text()="'+el[0]+'"]/Album[text()="'+el[1]+'"]/Song[text()="'+el[2]+'"]'))


class AMXML:
    def __init__(self):

        self.song_list = []  # List of lists, each list refers to a single song
        self.missing_songs = []
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
        self.root = ET.XML(ET.tostring(ET.parse(self.xml_path)))

        self.tolist()

    def checkpath(self, type="d"):
        """
        A minimal function for asking and validating a given path
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
        NB: This function is designed to extract informations from XML exported by Apple Music

        This function returns the inforamtion about every song
        in an array halted by a 'Remote' tag
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

        Takes a source directory in which search the songs and
        creates links to them inside a subfolder of the source directory, named as the XML file
        """
        self.missing_songs = []

        dst_path = os.path.join(
            self.path, os.path.splitext(os.path.basename(self.xml_path))[0] + "_link"
        )  # Folder in which place the links
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)

        for i in range(0, len(self.song_list)):
            # Check for the song at the path src_path/Author/Album/Song
            # bcs at the moment i'm converting the songs following this path convention
            art = "".join(regex.split('[:"/?]', self.song_list[i][0])).strip(
                '"'
            )  # Remove the symbols removed by the converter,
            alb = "".join(regex.split('[:"/?]', self.song_list[i][1])).strip(
                '"'
            )  # thus absent in the file names
            song = "".join(regex.split('[:"/?]', self.song_list[i][2])).strip('"')
            song_path = os.path.join(self.path, art, alb, song + ".mp3")

            if os.path.exists(song_path):  # and os.path.isfile(song_path):
                try:
                    if type == "s":
                        subprocess.call(
                            "ln -s "
                            + '"'
                            + song_path
                            + '"'
                            + " "
                            + '"'
                            + dst_path
                            + '"',
                            shell=True,
                        )  # Shell call to symlink the file
                    elif type == "c":
                        shutil.copy2(song_path, dst_path)  # Make a copy
                except Exception as e:
                    print(e)
            else:
                self.missing_songs.append([art, alb, song])

    def getmissing(self):
        """
        Get the Artists and their songs that are missing at a given path
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


# src = AMXML()

# src.missing_songs = []
# path = "/Volumes/MSDOS/Musica/1) Genres/R&B_Soul/"
# xml = "/Users/Roberto/Documents/R&B_Soul.xml"
# songs = "/Users/Roberto/Desktop/songs.xml"
# dst = ET.XML(ET.tostring(ET.parse(songs)))
#
# for i in range(0, len(src.song_list)):
#    # Check for the song at the path src_path/Author/Album/Song
#    # bcs at the moment i'm converting the songs following this path convention
#    art = "".join(regex.split('[:"/?]', src.song_list[i][0])).strip('"')
#    alb = "".join(regex.split('[:"/?]', src.song_list[i][1])).strip('"')
#    song = "".join(regex.split('[:"/?]', src.song_list[i][2])).strip('"')
#    if i == 724:
#        print((art, alb, song))
#    song_path = os.path.join(path, art, alb, song + ".mp3")
#    if not os.path.exists(song_path):
#        src.missing_songs.append([art, alb, song])
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
## Esplorando le missing songs di JB mi sono accorto che i brani contenenti lo slash nel nome in realta sono presenti nelle mie canzoni
## Il problema è anche lo slash, ridotto di 70 il numero
#
## FORSE C'è un problema con le lettere accentate (è,ù etc..), l'accento è di uno strano tipo in songs.xml
#
## Posso vedere quali sono glia Artisti in missign_songs e fare la stessa cosa che ho fatto per JB, aggregare le canzoni per artista e vedere i simboli che danno problemi
#
# for i in range(0, len(src.missing_songs)):
#    if src.missing_songs[i][0][:11] == "James Brown":
#        print((i, src.missing_songs[i]))
#
# arts = []  # Artists in AMXML
# for i in range(0, len(src.missing_songs)):
#    if src.missing_songs[i][0] not in arts:
#        arts.append(src.missing_songs[i][0])
#
# arts = np.sort(arts)
#
#
# arts_songs = {}
#
# for el in arts:
#    arts_songs[el] = []
#    for i in range(0, len(src.missing_songs)):
#        if (
#            src.missing_songs[i][0] == el
#        ):  # If the song matches the artist insert the song into the list
#            arts_songs[el].append([src.missing_songs[i][1], src.missing_songs[i][2]])
#
#
## arts_songs[arts[2]]  # List of the songs for the artist
#
## Now artist by artist i can detect the symbols and try to
## insert them into the regex and see if the missing_songs number lowers to the expected one of circa 200
# sym_arts = []
# for el in arts:
#    symbols = ""
#    for ele in arts_songs[el]:
#        for element in ele:
#            symbols = symbols + "".join(regex.split("[A-Za-z]", element))
#    sym_arts.append([symbols])
#
# i = 0
# for el in sym_arts:
#    print((i, el))
#    i = i + 1
#
#
# print(("Missing songs: ", len(src.missing_songs)))
# len(a)
#
