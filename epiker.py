#!/home/esmaeel/Applications/epiker/venv/bin/python
import os
import sys

from PyInquirer import prompt

from utils.functions import (crop, flip, get_action, resize, rotate,
                             same_parameters, select_images_to_edit,
                             which_images_to_edit, worker_crop, worker_flip,
                             worker_resize, worker_rotate, check_for_images)


print("welcome to CLI image editor v0.1")

ask_source_destination_folder = [
    {
        'type': 'input',
        'name': 'source_folder',
        'message': 'please enter address of folder which your pictures are in ("." for here) :>'
    },
    {
        'type': 'input',
        'name': 'destination_folder',
        'message': 'please enter destination folder you want to have your edited pictures in :>'
    },
]

answer_source_destination_folder = prompt(ask_source_destination_folder)

print("source folder : ", answer_source_destination_folder['source_folder'])
print("destination folder : ", answer_source_destination_folder['destination_folder'])

if not check_for_images(answer_source_destination_folder['source_folder']):
    print("There is no images in this direcotory, please try again")
    sys.exit()
    
if not os.path.exists(answer_source_destination_folder['destination_folder']) :
    print("creating destination directory...")

    os.mkdir(answer_source_destination_folder['destination_folder'])

    print("directory {} created successfully".format(answer_source_destination_folder['destination_folder']))

else:
    print("hopefully destination folder {} already exists.".format(answer_source_destination_folder['destination_folder']))

# 
images_to_edit = select_images_to_edit(answer_source_destination_folder['source_folder'])

actions = {
    'crop': crop,
    'flip': flip,
    'resize': resize,
    'rotate': rotate
}

action = get_action()

print("starting action ...")

actions[action](images_to_edit, answer_source_destination_folder)

print("done!")