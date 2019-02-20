from __future__ import print_function

import datetime
import json
import os.path
import sys

import pyexif


def main(argv):
    if len(argv) != 2:
        print('Usage: {} <directory containing photos_and_videos>'.format(argv[0]))
    basedir = argv[1]
    edited = 0
    unedited = 0
    for partial_image_path, timestamp in get_files_and_timestamps(os.path.join(basedir, 'photos_and_videos', 'moments.json')):
        image_path = os.path.join(basedir, partial_image_path)
        exif_editor = pyexif.ExifEditor(image_path)
        if exif_editor._getDateTimeField("DateTimeOriginal") is None:
            exif_editor.setOriginalDateTime(timestamp)
            edited += 1
        else:
            # This should use .getOriginalDateTime(), but the bug fix at
            # https://github.com/EdLeafe/pyexif/commit/600510a9266f30b63181e54cd10dc4e9879c0e73 has not been pushed to pip
            # yet.
            existing_timestamp = exif_editor._getDateTimeField("DateTimeOriginal")
            diff = abs(existing_timestamp - timestamp)
            if diff > datetime.timedelta(minutes=1):
                print(('WARNING: {} has a timestamp already ({}), but the timestamp in moments.json ({}) is different ' +
                       'by {}. If the photo was taken in a different time zone, this is expected.').format(
                           image_path, existing_timestamp, timestamp, diff))
            unedited += 1
    print('Done. Added timestamps to {} files, left {} untouched.'.format(edited, unedited))


def get_files_and_timestamps(path):
    with open(path, 'r') as f:
        json_contents = json.load(f)
        if json_contents.keys() != ['moments']:
            raise Exception('Surprising: '.format(json_contents.keys))
        for moment in json_contents['moments']:
            for photo in json_contents['moments'][moment]['photos']:
                yield (photo['uri'], datetime.datetime.fromtimestamp(photo['creation_timestamp']))

    
if __name__ == '__main__':
    main(sys.argv)
