# MusicManager

A Python program which lets you manage your stored music by using XML files.

## XML Manager

The script dir_to_xml.py lets you generate an XML tree of the songs stored on a device with the pattern Artist/Album/Song. 
Further, it makes possible to compare two directories to: 

- Find missing element of one folder wrt to another;
- Find shared elements between two folders;
- Merge the contents of a folder in another. 

The generation of the XML tree is a prior for the Python Daemon working correctly. 

#### Useful informations
-   The script has to be executed in a folder containing the pattern Artist/Album/Song.
-   The script will trail the blank spaces in the folders and files names introduced by AppleMacSoftDRM Converter.


## Python daemon
Since AppleMacSoft doesn't track the already convereted songs if you close the application, a daemon which does the work is necessary.
Make sure you have generated one or more XML of the songs already converted, thus stored on your device. 

The script fcheck.py has to be executed inside the directory in which the songs are being converted by AppleMacSoftDRM.

It will ask for the path of one or more XML files outputted by the XML Manager. 

These XML files will be used to stop the DRM converter when it finds the song being converted in one of the XML trees, moving to the next conversion.


## Apple Music XML Manager (AMXML)

This script lets you exploit XMLs exported by Apple Music to copy or create links to the songs already stored on your device with the pattern Artist/Album/Song.

Since organising hundreds or thousand of songs in playlists can be a tough and time-wasting work, you can use the script make_playlist_from_xml.py do it for you.
The purpose is to exploit the power of Apple Music' Smart playlists to organize your music library.

### Apple music playlist export

First you have to export the XML of a playlist from Apple Music: 

        File -> Library -> Export Playlist -> XML format

### AMXML usage

Now you can create an istance of the class AMXML (Apple Music XML):

        AMXML_object = AMXML(default=True)
    
With default = True it will ask for default settings regarding

-   The path of the Apple Music XML previously exported;
-   The path of the directory in which your songs are stored;

And will save them in a .txt file. If default=False the informations will be not saved.

NB: The latter must be structured as the "Genres" folder in the example below: 

    MyLibrary/
        Genres/
            R&B_Soul/
            Jazz/
            Hip-Hop/
            Rock/
            ...

The basic assumption is that the songs are first organized by musical Genres and then we can search accross all the genres for the songs in our playslist!

If you  DON'T want to follow this convention you can simply create an unique musical genre as follows: 

    MyLibrary/
        Genres/
            All_Genres_in_one/


Once instantied, the object will extract the information about every song in the XML file following the convention Artist/Album/Song.

### Operations
#### Link or copy the songs from the path source: 

    AMXML_object.tolink(type="s")

When **type="s"** will create symlinks to the songs stored on the device in a folder under the parent directory "Genres", named as the playlist.

    AMXML_object.tolink(type="c")


When **type="c"** will copy to the songs stored on the device in a folder under the parent directory "Genres", named as the playlist.
After invoking this function, **self.missing_songs** will be populated.

When **type** parameter differs from 'c' or 's' only the **self.missing_songs** will be populated.


#### Get the missing artists and their songs on your device with respect to the Apple Music XML playlist.

    artists, artists_songs = AMXML_object.getmissing()

After this function call you can access to: 

    AMXML_object.missing_songs
    len(AMXML_object.missing_songs)

in order to see an unstructered view of the missing songs and the total number of ones missing.

#### Find by Genre


#### Move by genre



### Possible problems and debugging

AppleMusicDRM Converter removes some symbols like **":\\?"** from the names of files, while Apple Music XML doesn't.
This creates ambiguity and some songs stored on your device might not be found from AMXML.

To overcome this problem always check that the number of songs in the playlist matches the number of links (or copies) created with AMXML.tolink().
If the numbers are different, you can explore the missing files by invoking: 

    artists, artists_songs = AMXML_object.getmissing()

and look for missing songs. 

It could happen that some songs are not really missing, this could be due to the ambiguity of the names explained before.
To find out what's causing the problem, simply invoke: 

   sym = AMXML_object.getsymbols()


You will get a list of symbols (non-alphabetic characters).
Check if one of them is not listed in **self.symbols** in the **AMXML.init()** and add it to the variable value; then try to execute again **AMXML.tolink()** and repeat this checking process.











