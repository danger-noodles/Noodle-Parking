#!/usr/bin/env python3

## IMPORTS

from openalpr import Alpr
import re
import sys


## FUNCTIONS

# Add hyphens to plates manually myself, since the API needs them
# https://github.com/openalpr/openalpr/issues/416
def add_hyphens(plate) -> str:
    count = re.findall(r'[0-9][A-Z]|[A-Z][0-9]', plate)

    if len(count) == 1:
        plate = re.sub(r'(..)(..)', '\\1-\\2', plate)
        plate = re.sub(r'-(..)(..)', '-\\1-\\2', plate)
    else:
        plate = re.sub(r'([0-9])([A-Z])', '\\1-\\2', plate)
        plate = re.sub(r'([A-Z])([0-9])', '\\1-\\2', plate)

    return(plate)

# This function converts and image to a string and returns an easy to use (for scripts) ditc
def image_to_list(image) -> list:
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
# TODO: Is there a better way of handling errors?
if not alpr.is_loaded():
    print('Error loading OpenALPR!')
    sys.exit(1)

# Specify the top N possibilities to return
alpr.set_top_n(5)

# Provide the library with the "nl" region for pattern matching
alpr.set_default_region('nl')

# TODO: For some reason this causes a SIGSEGV (Address boundary error)
#alpr.unload()
