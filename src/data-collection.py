# image_viewer.py

import io
import os
import FreeSimpleGUI as sg
from PIL import Image
import pandas as pd

def image_path_to_bytes(path):
    with Image.open(path) as img:
        with io.BytesIO() as byte_stream:
            img.save(byte_stream, format='PNG')
            byte_data = byte_stream.getvalue()
    return byte_data


def init(filename):
    # Get all filenames from the directory
    files = os.listdir("../data/ffn-training/celeba_1000")
    files.sort()

    # Create a DataFrame with filenames and their ratings
    data = {'Filename': files, 'Group': [0 for file in files], 'Group_rank': [0 for file in files], 'Rating': [0 for file in files]}
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def phase1(filename):

    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Current Image:"),
            sg.Text("", key="-IMAGE_NUMBER-"),
            sg.Text("Rating:"),
            sg.Text("", key="-RATING-"),
            sg.Button("Back")
        ],
    ]

    window = sg.Window("Face Value: Rating Phase", layout, return_keyboard_events=True, use_default_focus=False, finalize=True, element_justification='c')


    df = pd.read_csv(filename)

    index = 0
    while df.at[index, "Group"] != 0:
        index += 1
        if index == df.shape[0]:
            index = 0
            break

    loop = True
    while loop:

        window["-IMAGE_NUMBER-"].update(index + 1)
        window["-RATING-"].update(df.at[index, "Group"] if df.at[index, "Group"] != 0 else "")
        window["-IMAGE-"].update(data=image_path_to_bytes(f"../data/ffn-training/celeba_1000/{df.at[index, "Filename"]}"))

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            df.to_csv(filename, index=False)
            break
        elif event == "Back" and index >= 1:
            index -= 1
        elif event in "1234567890":
            df.at[index,"Group"] = int(event)
            index += 1
            if index == df.shape[0]:
                index = 0

    window.close()

#optional - only for very detailed 
def phase2(filename, group):

    layout = [
        [sg.Text("Which face is more attractive? ")], 
        [sg.Image(key="-IMAGEA-"), sg.Image(key="-IMAGEB-")],
        [
            sg.Text("Group:"),
            sg.Text(group, key="-GROUP-"),
            sg.Text("Progress:"),
            sg.Text("", key="-PROGRESS-"),
        ],
        [sg.Button("Left"), sg.Text("You may use the f and j buttons to make your selection"), sg.Button("Right")]
    ]

    window = sg.Window("Face Value: Sorting Phase", layout, return_keyboard_events=True, use_default_focus=False, finalize=True, element_justification='c')

    def merge_sort(arr, compare_func):

        def merge(left, right, compare_func):
            sorted_list = []
            i = j = 0
            while i < len(left) and j < len(right):
                if compare_func(left[i], right[j]) <= 0:
                    sorted_list.append(left[i])
                    i += 1
                else:
                    sorted_list.append(right[j])
                    j += 1
            sorted_list.extend(left[i:])
            sorted_list.extend(right[j:])
            return sorted_list

        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2

        left_half = merge_sort(arr[:mid], compare_func)
        right_half = merge_sort(arr[mid:], compare_func)
        return merge(left_half, right_half, compare_func)
    
    def compare_func(a, b):

        window["-IMAGEA-"].update(data=image_path_to_bytes(f"../data/ffn-training/celeba_1000/{a[0]}"))
        window["-IMAGEB-"].update(data=image_path_to_bytes(f"../data/ffn-training/celeba_1000/{b[0]}"))

        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                window.close()
            elif event in "asdf" or event=="Left":
                return 1
            elif event in "jkl;" or event=="Right":
                return -1


    df = pd.read_csv(filename)
    df_group = df.loc[df["Group"] == group]
    group_list = df.to_records(index=False).tolist()

    merge_sort(group_list, compare_func)

    window.close()





if __name__ == "__main__":
    #init("../data/ffn-training/ahc.csv")
    #phase1("../data/ffn-training/ahc.csv")
    phase2("../data/ffn-training/ahc.csv", 1)


