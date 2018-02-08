# youtube-dl-gui-simple


Since I tended to run only one command in youtube-dl and I hated going back and forth from the browser to the terminal, I wrote this script to run a PyQt4 Gui to run a youtube browser with a download buttions which will save videos to the "/Videos/" folder (or "/Music/" for audio).  The Gui is intended for a linux system.

NOTE: You must have the folders "/Videos/" and "/Music/" in your system.

## Screenshot
![alt text](https://raw.githubusercontent.com/jman27182818/youtube-dl-gui-simple/master/Screenshot.png)


## Requirements
* [Python 2.7.3+](https://www.python.org/downloads)
* [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)

## Running

download and extract source files to your desired directory.  Afterward run

    python2.7 youtubedlgui.py

A window will then appear with a youtube browser.  You can use the browser to navigate to your desired video.  Once you are there hit "Download" to start downloading the video to "~/Videos/".  

Checking "audio only" will just save the audio to "~/Music/".  The commands used to download are

    youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' --password PASSWORD -i -url 
    
for video and:

    youtube-dl --extract-audio --audio-format mp3 
    
for audio.  You can change these commands by editing the source file (change "str= ...").

NOTE: the built in textview only tracks when the download starts and when it completes.  To check the status, check the terminal.

## Multiple downloads

Currently only one download, or one playlist is supported.

## Creating a Launcher

If you desire you can create a launcher as described here (https://developer.gnome.org/integration-guide/stable/desktop-files.html.en)


    
