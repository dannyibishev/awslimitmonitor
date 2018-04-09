import json

class Color:
    """
    Colours used in errors function which help identify status' by colour.
    Options:

    RED, YELLOW, GREEN, BLUE, END """
    # Colours used in errors function which help identify status' by colour.
    RED = '\033[91m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    END = '\033[0m'

def pp_json(json_thing, sort=True, indents=4):
    """ function that works like print (Python 3), except it prints in a pretty json format | USED FOR DEBUGGING
    Usage:
        pp_json(response)
        pp_json(something_to_print)   # You get the idea.
    """
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents, default=str))
    return None

def status(new_input):
    """ Whatever is imported is converted to an integer and evaluated to return a STATUS response
    Usage:
        status("something_here")
    Returns: message   # Status e.g "--> STATUS = OKAY"
    """
    true_int = int(new_input)

    if true_int == 0:
        message = Color.BLUE + " --> THIS SERVICE IS NOT USED, NOTHING TO REPORT" + Color.END
    elif true_int <= 49:
        message = Color.GREEN + " --> STATUS = OKAY" + Color.END
    elif true_int >= 50 and true_int <= 74:
        message = Color.YELLOW + " --> STATUS = CAUTION, MAY REQUIRE LIMIT INCREASE SOON" + Color.END
    elif true_int >= 75:
        message = Color.RED + " --> STATUS = WARNING! APROACHING LIMIT, PLEASE INCREASE ASAP" + Color.END
    return message

def percentage(part, whole):
    """
    Divides a part number from a whole number.
    The final process is to round the number up and return it
    """
    return round(100 * float(part)/float(whole))
