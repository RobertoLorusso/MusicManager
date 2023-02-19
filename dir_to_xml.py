#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 01:29:14 2022

@author: Roberto
"""

import os
import sys
import shutil
from lxml import etree as ET
from distutils.dir_util import copy_tree


# TODO: Method for cleaning library from empty directories


class Dir:
    def __init__(self):

        self.root = ET.Element("root")
        input_text = ""
        b = True
        ex = False
        while b:
            try:
                print("Input path of directory or exit:")
                input_text = input()
                if os.path.isdir(os.path.abspath(input_text)):

                    input_text = os.path.abspath(input_text)
                    b = False
                elif input_text == "exit":
                    b = False
                    ex = True
                    sys.exit("Quitting...")

                else:
                    print("\nNot a valid path:" + str(input_text))
                    b = True
            except:
                print("\nBye!\n")

        if ex:
            exit(0)

        self.setpath(input_text)
        self.XMLPath = os.path.join(
            input_text, os.path.split(input_text)[1] + "ConvertedSongs.xml"
        )  # Output path
        self.trail()  # Remove blank spaces from directory and files names

    def __main__(self, write=True):

        if os.path.isdir(self.path):

            # Root element named as the folder for which we'll produce the XML
            start = ET.SubElement(self.root, "Genre", name=os.path.dirname(self.path))

            # Get the artists in the folder
            artists = sorted(
                [
                    dr
                    for dr in os.listdir(self.path)
                    if os.path.isdir(os.path.join(self.path, dr))
                ]
            )

            for a in artists:

                ar = ET.SubElement(
                    start, "Artist"
                )  # Create <Artist> Artist_Name </Artist>
                ar.text = a
                albums = sorted(
                    [
                        dr
                        for dr in os.listdir(
                            os.path.join(self.path, a)
                        )  # Get the dirs (Albums) under the current Artist
                        if os.path.isdir(
                            os.path.join(self.path, os.path.join(a, dr))
                        )  # Check they are dirs
                    ]
                )

                for album in albums:
                    songs = sorted(
                        [
                            dr
                            for dr in os.listdir(
                                os.path.join(
                                    self.path, os.path.join(a, album)
                                )  # Get the songs under the current Album
                            )
                            if os.path.isfile(
                                os.path.join(
                                    self.path,
                                    os.path.join(
                                        a, os.path.join(album, dr)
                                    ),  # Check they are files
                                )
                            )
                        ]
                    )
                    al = ET.SubElement(ar, "Album")  # create the tag Album:
                    al.text = album  # <Artist> Artist_Name <Album> Album_name </Album> </Artist>

                    for song in songs:
                        ET.SubElement(
                            al, "Song"
                        ).text = song  # append the songs inside the album tag

        self.tree = ET.ElementTree(self.root)
        ET.indent(self.root)

        if write:
            print(
                "There are "
                + str(len(self.root.xpath(".//Song")))
                + " songs in this folder"
            )
            self.tree.write(self.XMLPath, encoding="utf-8")
            print("\nFile output at: " + self.XMLPath)

    def trail(self):

        if os.path.isdir(self.path):

            artists = sorted(
                [
                    dr
                    for dr in os.listdir(self.path)
                    if os.path.isdir(os.path.join(self.path, dr))
                ]
            )

            for a in artists:

                os.rename(
                    os.path.join(self.path, a), os.path.join(self.path, a.strip())
                )
                a = a.strip()
                albums = sorted(
                    [
                        dr
                        for dr in os.listdir(os.path.join(self.path, a))
                        if os.path.isdir(os.path.join(self.path, os.path.join(a, dr)))
                    ]
                )

                for album in albums:

                    os.rename(
                        os.path.join(os.path.join(self.path, a), album),
                        os.path.join(os.path.join(self.path, a), album.strip()),
                    )
                    album = album.strip()

                    songs = sorted(
                        [
                            dr
                            for dr in os.listdir(
                                os.path.join(self.path, os.path.join(a, album))
                            )
                            if os.path.isfile(
                                os.path.join(
                                    self.path, os.path.join(a, os.path.join(album, dr))
                                )
                            )
                        ]
                    )

                    for song in songs:
                        os.rename(
                            os.path.join(
                                os.path.join(os.path.join(self.path, a), album), song
                            ),
                            os.path.join(
                                os.path.join(os.path.join(self.path, a), album),
                                song.strip(),
                            ),
                        )

    def setpath(self, inp):
        if os.path.isdir(inp):
            self.path = inp
            return True
        else:
            print("\nNot a valid directory: " + str(inp))
            return False

    def sharedElements(self, dst):

        for arsrc in self.tree.iter("Artist"):

            search = dst.tree.xpath('.//Artist[text()="' + arsrc.text + '"]')

            if len(search) > 0:

                for albsrc in arsrc.iter("Album"):
                    search = dst.tree.xpath(
                        './/Artist[text()="'
                        + arsrc.text
                        + '"]/Album[text()="'
                        + albsrc.text
                        + '"]'
                    )

                    # search = dst.tree.xpath('.//Album[text()="' + albsrc.text + '"]')

                    if len(search) > 0:

                        for songsrc in albsrc.iter("Song"):
                            search = dst.tree.xpath(
                                './/Artist[text()="'
                                + arsrc.text
                                + '"]/Album[text()="'
                                + albsrc.text
                                + '"]/Song[text()="'
                                + songsrc.text
                                + '"]'
                            )

                            # search = dst.tree.xpath('.//Song[text()="' + songsrc.text + '"]')
                            if len(search) > 0:

                                print("\t\t" + search[0].text)

    def diff(self, dst):

        for arsrc in self.tree.iter("Artist"):

            search = dst.tree.xpath('.//Artist[text()="' + arsrc.text + '"]')

            if len(search) == 0:

                print(arsrc.text)
            else:

                for albsrc in arsrc.iter("Album"):
                    search = dst.tree.xpath(
                        './/Artist[text()="'
                        + arsrc.text
                        + '"]/Album[text()="'
                        + albsrc.text
                        + '"]'
                    )

                    # search = dst.tree.xpath('.//Album[text()="' + albsrc.text + '"]')
                    if len(search) == 0:

                        print("\t" + albsrc.text)
                    else:

                        for songsrc in albsrc.iter("Song"):
                            search = dst.tree.xpath(
                                './/Artist[text()="'
                                + arsrc.text
                                + '"]/Album[text()="'
                                + albsrc.text
                                + '"]/Song[text()="'
                                + songsrc.text
                                + '"]'
                            )

                            # search = dst.tree.xpath('.//Song[text()="' + songsrc.text + '"]')
                            if len(search) == 0:

                                print("\t\t" + songsrc.text)

    def merge(self, dst):

        for arsrc in self.tree.iter("Artist"):

            search = dst.tree.xpath('.//Artist[text()="' + arsrc.text + '"]')

            if len(search) == 0:

                try:
                    copy_tree(
                        os.path.join(self.path, arsrc.text),
                        os.path.join(dst.path, arsrc.text),
                    )

                except Exception as e:

                    print("\nFailed in copying:" + arsrc.text)
                    print(str(e))
            else:

                for albsrc in arsrc.iter("Album"):

                    search = dst.tree.xpath(
                        './/Artist[text()="'
                        + arsrc.text
                        + '"]/Album[text()="'
                        + albsrc.text
                        + '"]'
                    )

                    if len(search) == 0:

                        try:

                            print(
                                os.path.isdir(
                                    os.path.join(
                                        os.path.join(self.path, arsrc.text), albsrc.text
                                    )
                                )
                            )
                            copy_tree(
                                os.path.join(
                                    os.path.join(self.path, arsrc.text), albsrc.text
                                ),
                                os.path.join(
                                    os.path.join(dst.path, arsrc.text), albsrc.text
                                ),
                            )

                        except Exception as e:
                            print("\nFailed in copying:" + albsrc.text)
                            print(str(e))
                    else:

                        for songsrc in albsrc.iter("Song"):

                            search = dst.tree.xpath(
                                './/Artist[text()="'
                                + arsrc.text
                                + '"]/Album[text()="'
                                + albsrc.text
                                + '"]/Song[text()="'
                                + songsrc.text
                                + '"]'
                            )

                            if len(search) == 0:

                                try:
                                    shutil.copy2(
                                        os.path.join(
                                            os.path.join(
                                                os.path.join(self.path, arsrc.text),
                                                albsrc.text,
                                            ),
                                            songsrc.text,
                                        ),
                                        os.path.join(
                                            os.path.join(dst.path, arsrc.text),
                                            albsrc.text,
                                        ),
                                    )

                                except Exception as e:
                                    print("\nFailed in copying:" + songsrc.text)
                                    print(str(e))


print("(1) XML generator\n(2) XML operations")
inp = input()
if inp == "1":

    wd = Dir()
    wd.__main__(write=True)

elif inp == "2":

    print("\nSource Directory:")
    src = Dir()
    print("\nDestination Directory")
    dst = Dir()
    src.__main__(False)
    dst.__main__(False)
    b = True
    while b:
        print(
            "\n(1) Show shared elements \n(2) Show Missing elements in Dest wrt Source \n(3) Merge Source in Destination \n(4) Exit"
        )
        inp = input()
        if inp == "1":
            print("\nShared elements:")
            src.sharedElements(dst)
        elif inp == "2":
            print("\nElements to copy from Source to Dest:")
            src.diff(dst)
        elif inp == "3":
            src.merge(dst)

        else:
            print("Exit?: [yes/no]")
            if str(input()).lower()[0] == "y":
                b = False
    sys.exit("See you!")


else:
    sys.exit("Quitting...")


#%% XML Test


# from lxml import etree as ET


# root = ET.Element("root")
# genre = ET.SubElement(root, "Genre", name = "Elettronica")

# jhon = ET.SubElement(genre, "Artist")
# jhon.text = "John Opkins"

# al = ["ALBUM1","ALBUM2"]
# for el in al:
#     album = ET.SubElement(jhon, "Album")
#     album.text = el
#     for i in range(0,10):
#         ET.SubElement(album, "Song").text = "canzone" + str(i)


# manu = ET.SubElement(genre, "Artist")
# manu.text = "Manu Chao"
# album = ET.SubElement(manu, "Album")
# album.text = "Bongo"

# for i in range(0,10):
#     ET.SubElement(album, "Song").text = "bongo" + str(i)


# album = ET.SubElement(manu, "Album")
# album.text = "Clandestino"

# for i in range(0,10):
#     ET.SubElement(album, "Song").text = "clandestino" + str(i)


# m = ET.SubElement(genre, "Artist")
# m.text = "Pino Daniele"
# album = ET.SubElement(m, "Album")
# album.text = "VAI mo"

# for i in range(0,10):
#     ET.SubElement(album, "Song").text = "vaimo" + str(i)


# tree = ET.ElementTree(root)
# ET.indent(root)


# tree.write("/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/test_songs.xml", encoding="utf-8")
