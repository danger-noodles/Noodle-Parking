#!/usr/bin/env python3

## IMPORTS

from openalpr import Alpr
import re
import sys


## FUNCTIONS

# Add hyphens to plates manually myself, since the API needs them
# https://github.com/openalpr/openalpr/issues/416
def add_hyphens(plate):
    count = re.findall(r'[0-9][A-Z]|[A-Z][0-9]', plate)

    if len(count) == 1:
        plate = re.sub(r'(..)(..)', '\\1-\\2', plate)
        plate = re.sub(r'-(..)(..)', '-\\1-\\2', plate)
    else:
        plate = re.sub(r'([0-9])([A-Z])', '\\1-\\2', plate)
        plate = re.sub(r'([A-Z])([0-9])', '\\1-\\2', plate)

    return(plate)

# This function converts the image to a string and prints it in formatted columns
# intended for command line use and easy debugging
def image_to_print(image):
    results = alpr.recognize_file(image)

    print(image)
    for plate in results['results']:
        print('   %12s %12s' % ('Plate', 'Confidence'))

        for candidate in plate['candidates']:
            region = '-'
            if candidate['matches_template']:
                region = '+'

                plate = add_hyphens(candidate['plate'])
            else:
                plate = candidate['plate']

            print("  %s %12s%12f" % (region, plate, candidate['confidence']))

# This function converts and image to a string and returns an easy to use (for scripts) ditc
def image_to_list(image):
    results = alpr.recognize_file(image)

    # TODO: Is this needed?
    if len(results['results']) == 0:
        return([])

    return_dict = []
    plate = results['results'][0]

    for candidate in plate['candidates']:
        region = False
        if candidate['matches_template']:
            region = True

            plate = add_hyphens(candidate['plate'])
        else:
            plate = candidate['plate']

        return_list = {
            'region': region,
            'plate': plate,
            'confidence': candidate['confidence'],
        }
        return_dict.append(return_list)

    return(return_dict)


## EXECUTE

# Initialize the library using European style license plates
alpr = Alpr('eu', './OpenALPR/Utils/openalpr.conf', './OpenALPR/Utils/runtime_data')
# TODO: is there a better way of handling errors?
if not alpr.is_loaded():
    print('Error loading OpenALPR!')
    sys.exit(1)

# Specify the top N possible plates to return
alpr.set_top_n(5)

# Provide the library with the "nl" region for pattern matching
alpr.set_default_region('nl')

# TODO: For some reason this causes a SIGSEGV (Address boundary error)
#alpr.unload()