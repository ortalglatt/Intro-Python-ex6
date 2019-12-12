import numpy
import math
import wave_helper

MAIN_CHOOSE_MSG = "Please choose what do you want to do: \n " \
                  "1. Change wav file \n 2. Merging 2 wav files \n " \
                  "3. Music composition in a wav file \n " \
                  "4. Go out of the program \n "
CHANGE_FILE = "1"
MERGE_FILES = "2"
COMPOSITION = "3"
OUT_OF_PROGRAM = "4"

CHANGE_FILE_MENU = "Please choose what do you want to do with the file: \n "\
                   "1. Reverse \n 2. Speed acceleration \n 3. Slow speed \n "\
                   "4. Increasing volume \n 5. Lowering volume \n " \
                   "6. Low pass filter \n "
REVERSE = "1"
HIGHER_SPEED = "2"
LOWER_SPEED = "3"
HIGHER_VOLUME = "4"
LOWER_VOLUME = "5"
LOW_PASS_FILTER = "6"

CHANGE_FILE_MSG = "Please enter the name of the file you want to change: "
MAX_VOLUME = 32767
MIN_VOLUME = -32768
VOLUME_CHANGE_CONST = 1.2

MERGE_MSG = "Please enter two names of the files you want to merge: "

COMPO_MSG = "Please enter the name of the composition instructions file: "
SCORES = {"C": 523, "D": 587, "E": 659, "F": 698, "G": 784, "A": 440,
          "B": 494}
QUIET = "Q"
LETTER_IN_SUBLIST = 0
NUM_IN_SUBLIST = 1
SAMPLE_RATE = 2000
AUDIO_CONST = 125

GO_MENU_MSG = "Please choose: \n 1. Save the audio \n " \
              "2. Change the audio \n "
SAVE_AUDIO = "1"
CHANGE_AUDIO = "2"
SAVE_MSG = "Please enter the name of the file you want to save: "

FRAME_IN_WAVE = 0
AUDIO_IN_WAVE = 1
INVALID_INPUT_MSG = "Invalid input, please try again."
PROBLEM_IN_FILE = -1
PROBLEM_MSG = "There was a problem with the file, please try again."


def main():
    user_choose = input(MAIN_CHOOSE_MSG)
    while user_choose not in [CHANGE_FILE, MERGE_FILES, COMPOSITION,
                              OUT_OF_PROGRAM]:
        print(INVALID_INPUT_MSG)
        user_choose = input(MAIN_CHOOSE_MSG)
    if user_choose == CHANGE_FILE:
        change_file()
    elif user_choose == MERGE_FILES:
        merge_files()
    elif user_choose == COMPOSITION:
        composition()


def change_file():
    """This function will open the changing file menu and check if
    input is valid. If so, I will send it to another function
    that will take care of the input and after the return it directs
    to the transit menu for further decisions."""
    filename = input(CHANGE_FILE_MSG)
    wave = wave_helper.load_wave(filename)
    while wave == PROBLEM_IN_FILE:
        print(PROBLEM_MSG)
        filename = input(CHANGE_FILE_MSG)
        wave = wave_helper.load_wave(filename)
    change_checked_file(wave)


def change_checked_file(wave):
    """In this function the user chooses what he wants to do with
    the file, and if the input is correct (no. 1 to 6) it makes
    the chosen change on the audio data list. It returns
    the new information to the previous function for further
    instructions."""
    user_input = input(CHANGE_FILE_MENU)
    while user_input not in [REVERSE, HIGHER_SPEED, LOWER_SPEED,
                             HIGHER_VOLUME, LOWER_VOLUME, LOW_PASS_FILTER]:
        print(INVALID_INPUT_MSG)
        user_input = input(CHANGE_FILE_MENU)
    frame_rate = wave[FRAME_IN_WAVE]
    audio_data = wave[AUDIO_IN_WAVE]
    if user_input == REVERSE:
        audio_data = reverse(audio_data)
    elif user_input == HIGHER_SPEED:
        audio_data = higher_speed(audio_data)
    elif user_input == LOWER_SPEED:
        audio_data = lower_speed(audio_data)
    elif user_input == HIGHER_VOLUME:
        audio_data = higher_volume(audio_data)
    elif user_input == LOWER_VOLUME:
        audio_data = lower_volume(audio_data)
    elif user_input == LOW_PASS_FILTER:
        audio_data = low_pass_filter(audio_data)
    transit_menu([frame_rate, audio_data])


def reverse(audio_data):
    """This function get a list, and return the same list in the apposite
    order."""
    reverse_audio_data = audio_data[::-1]
    return reverse_audio_data


def higher_speed(audio_data):
    """This function gets a list, and returns a new shorter list, that contains
    only the arguments that their index in the original list is even."""
    new_audio_data = list()
    new_audio_len = int(len(audio_data) / 2 + 0.5)
    for i in range(new_audio_len):
        new_audio_data.append(audio_data[2 * i])
    return new_audio_data


def lower_speed(audio_data):
    """This function gets a list of sub-lists, and return a new longer list.
    the new list contains the same arguments from the original list, and
    between every 2 arguments, it inserts a new sublist that contains the
    averages of the numbers the 2 arguments contain."""
    new_audio_data = list()
    for i in range(len(audio_data) - 1):
        new_audio_data.append(audio_data[i])
        new_sublist = average_sublist([audio_data[i], audio_data[i + 1]])
        new_audio_data.append(new_sublist)
    new_audio_data.append(audio_data[-1])
    return new_audio_data


def average_sublist(sublists_list):
    """This function gets a list of lists and creates 2 new lists,
    one from the inner left arguments, and second from the right ones.
    This function makes the average actions over lists more efficient,
    because it can calculate over as many arguments as needed, in the
    given list."""
    left_list = list()
    right_list = list()
    for i in range(len(sublists_list)):
        left_list.append(sublists_list[i][0])
        right_list.append(sublists_list[i][1])
    left_num = int(numpy.mean(left_list))
    right_num = int(numpy.mean(right_list))
    return [left_num, right_num]


def higher_volume(audio_data):
    """This function creates a new audio data list by multiplying every
    argument on the list by 1.2 and returning the new list. Making
    sure that the absolute maximum will not be passed."""
    new_audio_data = list()
    for i in range(len(audio_data)):
        num1 = int(audio_data[i][0] * VOLUME_CHANGE_CONST)
        num2 = int(audio_data[i][1] * VOLUME_CHANGE_CONST)
        sublist = [volume_fix(num1), volume_fix(num2)]
        new_audio_data.append(sublist)
    return new_audio_data


def volume_fix(num):
    """This short function makes sure that the maximum or minimum
    is not reached, with fixed max and min volumes, given a number."""
    num = min(num, MAX_VOLUME)
    num = max(num, MIN_VOLUME)
    return num


def lower_volume(audio_data):
    """This function reduces the rates of a given list by
    a 1.2 factor, in order to reduce the volume, and return it."""
    new_audio_data = list()
    for i in range(len(audio_data)):
        num1 = int(audio_data[i][0] / VOLUME_CHANGE_CONST)
        num2 = int(audio_data[i][1] / VOLUME_CHANGE_CONST)
        new_audio_data.append([num1, num2])
    return new_audio_data


def low_pass_filter(audio_data):
    """This function does the fade away effect over a given audio data.
    The function is divided into 2 parts, because it has to differ between
    2 cases: Changing the first and last couple of arguments, and using
    another function to change the arguments that are not first or last"""
    length = len(audio_data) - 1
    first_sublist = [average_sublist([audio_data[0], audio_data[1]])]
    mid_list = mid_sublists_filter(audio_data)
    last_sublist = [average_sublist([audio_data[length - 1],
                                     audio_data[length]])]
    new_audio_data = first_sublist + mid_list + last_sublist
    return new_audio_data


def mid_sublists_filter(audio_data):
    """This function runs over a list between the first and last arguments
    and creates a new sublist by calculating the average of every
    3 following arguments."""
    mid_list = list()
    for i in range(1, len(audio_data) - 1):
        first = audio_data[i - 1]
        second = audio_data[i]
        third = audio_data[i + 1]
        sublist = average_sublist([first, second, third])
        mid_list.append(sublist)
    return mid_list


def merge_files():
    """This function asks the user for 2 wav files to combine. It checks
    that the input file exists and then uses a a function to create a new
    list from the 2 lists given, and it returns it along with the lower
    frame rate to the transit menu."""
    filenames = input(MERGE_MSG)
    while filenames.count(" ") != 1:
        print(PROBLEM_MSG)
        filenames = input(MERGE_MSG)
    filenames = filenames.split(" ")
    wave1 = wave_helper.load_wave(filenames[0])
    wave2 = wave_helper.load_wave(filenames[1])
    while wave1 == PROBLEM_IN_FILE or wave2 == PROBLEM_IN_FILE:
        print(PROBLEM_MSG)
        filenames = input(MERGE_MSG).split(" ")
        wave1 = wave_helper.load_wave(filenames[0])
        wave2 = wave_helper.load_wave(filenames[1])
    gcd_num = math.gcd(wave1[FRAME_IN_WAVE], wave2[FRAME_IN_WAVE])
    new_audio_data = create_new_list(wave1, wave2, gcd_num)
    minimum_rate = min(wave1[FRAME_IN_WAVE], wave2[FRAME_IN_WAVE])
    transit_menu([minimum_rate, new_audio_data])


def create_new_list(wave1, wave2, gcd_num):
    """This function is there to indicate which frame rate is lower, it then
    finds the gcd of both frame rate. Then the list of the higher frame
    rate needs to be changed with the list_after_gcd function, and then the
    fixed list and the original list of the lower frame rate go together
    to a function that combines them to a new list."""
    if wave1[FRAME_IN_WAVE] > wave2[FRAME_IN_WAVE]:
        maximum = wave1[FRAME_IN_WAVE] / gcd_num
        minimum = wave2[FRAME_IN_WAVE] / gcd_num
        audio_data1 = list_after_gcd(wave1[AUDIO_IN_WAVE], maximum, minimum)
        # the faster rate goes through a change
        audio_data2 = wave2[AUDIO_IN_WAVE]
        # stays original
        new_list = merge_lists(audio_data1, audio_data2)
        # both lists go to a combine function
    elif wave2[FRAME_IN_WAVE] > wave1[FRAME_IN_WAVE]:
        minimum = wave1[FRAME_IN_WAVE] / gcd_num
        maximum = wave2[FRAME_IN_WAVE] / gcd_num
        audio_data2 = list_after_gcd(wave2[AUDIO_IN_WAVE], maximum, minimum)
        # the faster rate goes through a change
        audio_data1 = wave1[AUDIO_IN_WAVE]
        # stays original
        new_list = merge_lists(audio_data1, audio_data2)
        # both lists go to a combine function
    else:
        new_list = merge_lists(wave1[AUDIO_IN_WAVE], wave2[AUDIO_IN_WAVE])
        # if the frame rate is equal, both lists go to combine
        # function in the original form
    return new_list


def list_after_gcd(audio_data, maximum, minimum):
    """Given max and min values, this list cuts off the indexes in the list
    that should not be there, in the given list, which is the list connected
    to the higher frame_rate from the create_new_list function"""
    new_list = list()
    for i in range(len(audio_data)):
        if minimum > i % maximum:
            new_list.append(audio_data[i])
    return new_list


def merge_lists(list_1, list_2):
    """Given 2 fixed lists, this function combines them in the following
    system: it does the average of respective indexes, until one of the
    list is done, and then it puts the leftovers of the longer list as is."""
    new_list = list()
    minimum = min(len(list_1), len(list_2))
    for i in range(minimum):
        sublist = average_sublist([list_1[i], list_2[i]])
        new_list.append(sublist)
        # adding the average sublist as long as they are equal indexes
    if len(list_1) > len(list_2):
        # if the first list is longer, it continues adding its arguments
        new_list += list_1[minimum:]
    elif len(list_1) < len(list_2):
        # if the second list is longer, it continues adding its arguments
        new_list += list_2[minimum:]
    return new_list


def composition():
    """This function opens the given text file and create a string out of it.
    then it uses string_to_compo_list to create a list in the form of
    [char, times]. Then it goes for every argument in the list that
    contains a char and the amount of samples it has to create, and adds it
    to the audio data list."""
    filename = input(COMPO_MSG)
    file = open(filename)
    string = ""
    for line in file:
        string += " " + line.strip()
    compo_list = string_to_compo_list(string)
    # creating the list of the string in the file
    audio_data = list()
    for sublist in compo_list:
        audio_data = compo_sublist(sublist, audio_data)
        # uses compo_sublist to update the audio data list
    transit_menu([SAMPLE_RATE, audio_data])


def string_to_compo_list(string):
    """This function takes a string and returns list of 2 arguments lists,
    where the left argument is a letter (A-G,Q) and the right argument is
    the amount of samples has to be taken."""
    lst = string.split()
    length = int(len(lst) / 2)
    new_list = list()
    for i in range(length):
        sublist = [lst[2 * i], int(lst[2 * i + 1])]
        # even index is the letter, odd is a number
        new_list.append(sublist)
    return new_list


def compo_sublist(sublist, audio_data):
    """This function analyses the sublist with the letter and amount of samples
    and creates a list that should be added to the main audio data list.
    If the char is Q it has to add specific pairs, [0,0]"""
    letter = sublist[LETTER_IN_SUBLIST]
    num = sublist[NUM_IN_SUBLIST]
    times = num * AUDIO_CONST
    if letter == QUIET:
        audio_data += [[0, 0]] * times
    else:
        for i in range(times):
            sample_val = int(sample_value(i, letter))
            # uses sample_value function to get the frequent to add
            audio_data.append([sample_val, sample_val])
    return audio_data


def sample_value(i, letter):
    """This function uses the dictionary and with the formula given in the
    tirgul it calculates the sample value"""
    freq = SCORES.get(letter)
    samples_per_cycle = SAMPLE_RATE / freq
    num = MAX_VOLUME * math.sin(2 * math.pi * (i / samples_per_cycle))
    return num


def transit_menu(wave):
    """After every change to the given or created file, this menu will tell
    if the user wants to save, and then go to main menu, or keep changing
    the file."""
    frame_rate = wave[FRAME_IN_WAVE]
    audio_data = wave[AUDIO_IN_WAVE]
    user_input = input(GO_MENU_MSG)
    while user_input not in [SAVE_AUDIO, CHANGE_AUDIO]:
        print(INVALID_INPUT_MSG)
        user_input = input(GO_MENU_MSG)
    if user_input == SAVE_AUDIO:
        filename = input(SAVE_MSG)
        wave_helper.save_wave(frame_rate, audio_data, filename)
        main()
    else:
        change_checked_file([frame_rate, audio_data])


if __name__ == "__main__":
    main()

