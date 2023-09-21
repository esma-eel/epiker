import os
import sys

from PIL import Image
from PyInquirer import prompt

# image formats supported
image_formats = ['jpg', 'png', 'jpeg', 'gif', 'svg']

# checks if there is any image in the given directory
def check_for_images(folder):
    images = []
    for file in os.listdir(folder):
        for fmt in image_formats:
            if file.endswith(fmt):
                images.append(file)
    
    return images

# main workder for listing and selecting images
def which_images_to_edit(source_folder):
    list_of_images_name = check_for_images(source_folder)
   
    if not list_of_images_name:
        print("There is no images in this direcotory, please try again")
        sys.exit()

    ask_which_images = [
        {
            'type': 'checkbox',
            'message': 'select at least one of pictures below to edit :> ',
            'name': 'raw_images',
            'choices': [
                {"name": image_name} for image_name in list_of_images_name
            ],
        }
    ]

    answer_which_images = prompt(ask_which_images)
    
    return answer_which_images['raw_images']

# select which images to edit and confirm if you want to continue or select again
def select_images_to_edit(source_folder):
    answer_continue_or_select_again = {}
    which_images = []
    ask_continue_or_select_again = [
        {
            'type': 'rawlist',
            'message': 'do you want to continue or select again ? ',
            'name': 'continue_or_select_again',
            'choices': [
                'continue',
                'select_again'
            ]
        }
    ]

    answer_continue_or_select_again['continue_or_select_again'] = "select_again"
    while not answer_continue_or_select_again['continue_or_select_again'] == "continue":
        which_images = which_images_to_edit(source_folder)
        print("you selected these pictures to edit :")
        print(which_images)

        answer_continue_or_select_again = prompt(ask_continue_or_select_again)
    
    return which_images

# asks users which action they want and they can select those with 
# c(crop), f(Flip), r(Rotate), z(Resize)
def get_action():
    ask_which_action = [
        {
            'type': 'expand',
            'message': 'which action do you want to apply to your images ? press (h) to see all actions.',
            'default': 'h',
            'name': 'action',
            'choices': [
                {
                    'key': 'c',
                    'value': 'crop',
                    'name': 'Crop',
                },
                {
                    'key': 'f',
                    'value': 'flip',
                    'name': 'Flip',
                },
                {
                    'key': 'r',
                    'value': 'rotate',
                    'name': 'Rotate',
                },
                {
                    'key': 'z',
                    'value': 'resize',
                    'name': 'Resize',
                },
            ],
            
        }
    ]

    answer_which_action = prompt(ask_which_action)
    print('you wanted to %s your images.'%(answer_which_action['action']))

    return answer_which_action['action']

# final action of crop
def worker_crop(image, top_left, top_right, bottom_right, bottom_left, source_destination_folder):
    
    croppedIm = image.crop((top_left, top_right, bottom_right, bottom_left))

    croppedIm.save(source_destination_folder['destination_folder']+'/'+image.filename.replace(source_destination_folder['source_folder'], '')+"_crop.jpeg")
    # os.path.join(source_destination_folder['destination_folder'], image.filename.replace(source_destination_folder['source_folder'], '')+"_%s.jpeg"%(action))

# final action of flip
def worker_flip(image, direction, source_destination_folder):

    flipedIm = image.transpose(direction)

    flipedIm.save(source_destination_folder['destination_folder']+'/'+image.filename.replace(source_destination_folder['source_folder'], '')+"_flip.jpeg")

# final action of rotate
def worker_rotate(image, degree, source_destination_folder):
    rotatedIm = image.rotate(int(degree), expand=True)

    rotatedIm.save(source_destination_folder['destination_folder']+'/'+image.filename.replace(source_destination_folder['source_folder'], '')+"_rotate.jpeg")

# final action of resize
def worker_resize(image, width, height, source_destination_folder):
    resizedIm = image.resize((int(width), int(height)))

    resizedIm.save(source_destination_folder['destination_folder']+'/'+image.filename.replace(source_destination_folder['source_folder'], '')+"_resize.jpeg")

# check if you want to edit your pictures with same parameters or diffrent ones for each image
def same_parameters():
    ask_same_or_different = [
        {
            'type': 'list',
            'name': 'same_or_different',
            'message': 'work on all of images with same parameters or different for each pic ? :> ',
            'choices': [
                {'name': 'same', 'value': True},
                {'name': 'different', 'value': False}
            ]
        }
    ]

    answer_same_or_different = prompt(ask_same_or_different)

    return answer_same_or_different['same_or_different']


# intiatiing crop functionality
def crop(images_to_edit, source_destination_folder):
    ask_crop_parameters = [
    {
            'type': 'input',
            'name': 'top_left',
            'message': 'please enter top_left point :>'
        },
        {
            'type': 'input',
            'name': 'top_right',
            'message': 'please enter top_right point :>'
        },
        {
            'type': 'input',
            'name': 'bottom_right',
            'message': 'please enter bottom_right point :>'
        },
        {
            'type': 'input',
            'name': 'bottom_left',
            'message': 'please enter bottom_left point :>'
        },
    ]

    answer_crop_parameters = None
    same = same_parameters()
    if same:
        print("parameters for ", images_to_edit)
        answer_crop_parameters = prompt(ask_crop_parameters)
    # answer_same_or_different['same_or_different']
    for image in images_to_edit:
        image = Image.open(os.path.join(source_destination_folder['source_folder'], image))
        if not same:
            print("parameters for {name} , numbers must be between {width}x{height}".format(name=image.filename, width=image.size[0], height=image.size[1]))
            answer_crop_parameters = prompt(ask_crop_parameters)

        worker_crop(image, int(answer_crop_parameters['top_left']), int(answer_crop_parameters['top_right']), int(answer_crop_parameters['bottom_right']), int(answer_crop_parameters['bottom_left']), source_destination_folder)

# intiatiing flip functionality
def flip(images_to_edit, source_destination_folder):
    ask_flip_parameters = [
        {
            'type': 'list',
            'name': 'direction',
            'message': 'flip (Left to Right) or (Top to Bottom) :> ',
            'choices': [
                {'name': 'Left To Right', 'value': Image.FLIP_LEFT_RIGHT},
                {'name': 'Top to Bottom', 'value': Image.FLIP_TOP_BOTTOM},
            ]
        }
    ]

    answer_flip_parameters = None
    same = same_parameters()
    if same:
        print("parameters for ", images_to_edit)
        answer_flip_parameters = prompt(ask_flip_parameters)
    
    for image in images_to_edit:
        image = Image.open(os.path.join(source_destination_folder['source_folder'], image))
        if not same:
            print("Flip Image {name}:".format(name=image.filename))
            answer_flip_parameters = prompt(ask_flip_parameters)

        worker_flip(image, answer_flip_parameters['direction'], source_destination_folder)

# intiatiing rotate functionality
def rotate(images_to_edit, source_destination_folder):
    ask_rotate_parameters = [
        {
            'type': 'input',
            'name': 'degree',
            'message': 'how many degrees you want to rotate :> ',
        }
    ]

    answer_rotate_parameters = None
    same = same_parameters()
    if same:
        print("parameters for ", images_to_edit)
        answer_rotate_parameters = prompt(ask_rotate_parameters)
    
    for image in images_to_edit:
        image = Image.open(os.path.join(source_destination_folder['source_folder'], image))
        if not same:
            print("how many degrees to rotate image {name} :".format(name=image.filename))
            answer_rotate_parameters = prompt(ask_rotate_parameters)

        worker_rotate(image, answer_rotate_parameters['degree'], source_destination_folder)

# intiatiing resize functionality
def resize(images_to_edit, source_destination_folder):
    ask_resize_parameters = [
        {
            'type': 'input',
            'name': 'width',
            'message': 'enter new width :> ',
        },
        {
            'type': 'input',
            'name': 'height',
            'message': 'enter new height :> ',
        },
    ]

    answer_resize_parameters = None
    same = same_parameters()
    if same:
        print("parameters for ", images_to_edit)
        answer_resize_parameters = prompt(ask_resize_parameters)
    
    for image in images_to_edit:
        image = Image.open(os.path.join(source_destination_folder['source_folder'], image))
        if not same:
            print("enter new width, height for image {name} :".format(name=image.filename))
            answer_resize_parameters = prompt(ask_resize_parameters)

        worker_resize(image, answer_resize_parameters['width'], answer_resize_parameters['height'], source_destination_folder)
