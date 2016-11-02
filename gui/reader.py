
from openalpr import Alpr
import sys

## FUNCTIONS

# This function converts the image to a string and prints it in formatted columns
# intended for command line use and easy debugging
def image_to_print(image):
    results = alpr.recognize_file(image)

    i = 0
    for plate in results['results']:
        i += 1

        print('Plate #%d:' % i)
        print('   %12s %12s' % ('Plate', 'Confidence'))

        for candidate in plate['candidates']:
            region = '-'
            if candidate['matches_template']:
                region = '+'

            print("  %s %12s%12f" % (region, candidate['plate'], candidate['confidence']))

# This function converts and image to a string and returns an easy to use (for scripts) ditc
def image_to_list(image):
    results = alpr.recognize_file(image)

    return_dict = []
    i = 0
    for plate in results['results']:
        i += 1

        for candidate in plate['candidates']:
            region = False
            if candidate['matches_template']:
                region = True

            return_list = {
                'region': region,
                'plate': candidate['plate'],
                'confidence': candidate['confidence'],
            }
            return_dict.append(return_list)

    return(return_dict)


## EXECUTE

# Initialize the library using European style license plates
alpr = Alpr('eu', './openalpr/openalpr.conf', './openalpr/runtime_data')
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
