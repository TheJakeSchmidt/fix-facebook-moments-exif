# Overview

Facebook Moments is being shut down on February 25. Facebook has provided the option to download
your Moments as a .zip file, but (presumably because *computers were a mistake*) the timestamps have
been stripped from some of the images' EXIF data. At a glance, which files are missing data does not
appear to be correlated with date, moment, or source, and is definitely missing from some photos I
uploded from my camera that have EXIF data in the original. It seems random.

Fortunately, Facebook included the timestamps in a separate moments.json file that's included with
the download. The script in this repository will read the moments.json and restore the timestamps to
the EXIF data.

# Usage

I only tested on Linux, but I think the script will work on other operating systems if exiftool and
pyexif are installed. These instructions assume you unzipped the `facebook-yourusername.zip` file in
the directory /home/yourusername/Downloads, such that /home/yourusername/Downloads/photos_and_videos
contains the moments.json file.

```
$ sudo apt install exiftool
$ pip install pyexif
$ git clone https://github.com/TheJakeSchmidt/fix-facebook-moments-exif.git
$ cd fix-facebook-moments-exif
$ python fix_facebook_moments_exif.py /home/yourusername/Downloads
```

And, if you have a GPS track file (for example, from your Google Location History), you might want
to add locations with exiftool:

```
$ exiftool -geotag <directory>/Location\ History.kml photos_and_videos/moments/*/*.jpg
```
