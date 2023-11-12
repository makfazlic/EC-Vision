print("""
####################### Welcome to the EC Vision ###########################
      
 ________   ______          __     __  __            __                     
/        | /      \        /  |   /  |/  |          /  |                    
$$$$$$$$/ /$$$$$$  |       $$ |   $$ |$$/   _______ $$/   ______   _______  
$$ |__    $$ |  $$/ ______ $$ |   $$ |/  | /       |/  | /      \ /       \ 
$$    |   $$ |     /      |$$  \ /$$/ $$ |/$$$$$$$/ $$ |/$$$$$$  |$$$$$$$  |
$$$$$/    $$ |   __$$$$$$/  $$  /$$/  $$ |$$      \ $$ |$$ |  $$ |$$ |  $$ |
$$ |_____ $$ \__/  |         $$ $$/   $$ | $$$$$$  |$$ |$$ \__$$ |$$ |  $$ |
$$       |$$    $$/           $$$/    $$ |/     $$/ $$ |$$    $$/ $$ |  $$ |
$$$$$$$$/  $$$$$$/             $/     $$/ $$$$$$$/  $$/  $$$$$$/  $$/   $$/ 
""")




import argparse
from helpers import *
import warnings
import pandas as pd
import os
import shutil

import csv_helpers

#### Output is in output-last-run folder
#### We have to clear it if it exists
if os.path.exists('output-last-run'):
    shutil.rmtree('output-last-run')

warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser(description='EC Vision')
parser.add_argument('-m', '--mode', type=str, required=True, help='Logo or Face')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file or folder (only csv files)')

args = parser.parse_args()

if args.mode == 'face':
    print_bar('1.')
    print_bar('Running the face module')
    print()
    print_bar('2.')
    starting_folder = ""
    if args.input.endswith('.csv'):
        print('[Received] Input file type: csv, Input path:', args.input)
        headers_csv = csv_helpers.get_csv_headers(args.input)
        print("📝 Headers in the csv file:")
        for i, header in enumerate(headers_csv):
            print(f'{i}: {header}')
        csv_index = int(input("Write the index of the column with image urls: "))
        name_columns = input("Write the indices of the columns to be used as names of output (separated by space): ")
        
        name_columns = [int(i) for i in name_columns.split()]
        image_urls = csv_helpers.get_csv_column(args.input, csv_index)  

        names = []
        for i, name_column in enumerate(name_columns):
            this_col_names = csv_helpers.get_csv_column(args.input, name_column)
            this_col_names = [name.replace(' ', '_') for name in this_col_names]
            this_col_names = [name.lower() for name in this_col_names]
            names.append(this_col_names)

        names = list(zip(*names))
        names = ['_'.join(name) for name in names]
        print_bar('Starting to download images')
        starting_folder = csv_helpers.save_urls_to_folder(image_urls, names)

    else:
        print('[Received] Input file type: folder, Input path:', args.input)
        starting_folder = args.input

    
    print('Input resolved, using folder: ' + starting_folder + ' with ' + str(files_in_folder(starting_folder)) + ' files')
    print()
    print_bar('3.')
    size = input('Enter the size of the image (default: 500 pixels) or "Enter" to accept default: ')
    if size == '':
        size = 500
    else :
        size = int(size)
    print('[Received] Input size: {}x{}'.format(size, size))
    print('Size of images to work with resolved')
    print()

    print_bar('4.')
    print_bar('Creating a folder to work with')

    saved_init_starting_folder = starting_folder
    shutil.copytree(starting_folder, 'output-last-run')
    starting_folder = 'output-last-run/'


    print('Folder created, starting to work with images in folder: output-last-run/1-original')
    print()

    print_bar('5.')
    print_bar('Starting to detect and center faces to 1:1')
    center_faces(starting_folder)
    init_size = calculate_size(starting_folder)

    print()

    print_bar('6.')
    print_bar('Cropping faces to '+str(size)+'x'+str(size))
    crop_images(starting_folder, size, size)
    print()

    print_bar('7.')
    print_bar('Webp conversion')
    convert_to_webp(starting_folder)
    print()
    final_size = calculate_size(starting_folder)

    print_bar('DONE!')
    print('Initial size: {} MB'.format(round(init_size / 1024 / 1024, 2)))
    print('Final size: {} MB'.format(round(final_size / 1024 / 1024, 2)))
    change = abs(((final_size - init_size) / init_size) * 100)
    print('🏆 Total size saved: {} MB ({}%)'.format(round((init_size - final_size) / 1024 / 1024, 2), round(change, 2)))
    print()
    not_handled = get_diffrent_files(saved_init_starting_folder, starting_folder)
    print('🚫 Not handled files: ' + str(not_handled))
    

elif args.mode == 'logo':
    print_bar('1.')
    print_bar('Running the logo module')
    print()
    print_bar('2.')
    starting_folder = ""
    if args.input.endswith('.csv'):
        print('[Received] Input file type: csv, Input path:', args.input)
        headers_csv = csv_helpers.get_csv_headers(args.input)
        print("📝 Headers in the csv file:")
        for i, header in enumerate(headers_csv):
            print(f'{i}: {header}')
        csv_index = int(input("Write the index of the column with image urls: "))
        name_columns = input("Write the indices of the columns to be used as names of output (separated by space): ")
        
        name_columns = [int(i) for i in name_columns.split()]
        image_urls = csv_helpers.get_csv_column(args.input, csv_index)  

        names = []
        for i, name_column in enumerate(name_columns):
            this_col_names = csv_helpers.get_csv_column(args.input, name_column)
            this_col_names = [name.replace(' ', '_') for name in this_col_names]
            this_col_names = [name.lower() for name in this_col_names]
            names.append(this_col_names)

        names = list(zip(*names))
        names = ['_'.join(name) for name in names]
        print_bar('Starting to download images')
        starting_folder = csv_helpers.save_urls_to_folder(image_urls, names)

    else:
        print('[Received] Input file type: folder, Input path:', args.input)
        starting_folder = args.input

    
    print('Input resolved, using folder: ' + starting_folder + ' with ' + str(files_in_folder(starting_folder)) + ' files')
    print()

    print_bar('3.')
    size_w = input('Enter the width of the image (default: 500 pixels) or "Enter" to accept default: ')
    if size_w == '':
        size_w = 500
    else :
        size_w = int(size_w)
    size_h = input('Enter the height of the image (default: 500 pixels) or "Enter" to accept default: ')
    if size_h == '':
        size_h = 500
    else :
        size_h = int(size_h)
    print('[Received] Input size: {}x{}'.format(size_w, size_h))
    print('Size of images to work with resolved')    
    print()

    print_bar('4.')
    print_bar('Creating a folder to work with')

    saved_init_starting_folder = starting_folder
    init_size = calculate_size(saved_init_starting_folder)
    shutil.copytree(starting_folder, 'output-last-run/1-original')
    starting_folder = 'output-last-run/1-original'

    print('Folder created, starting to work with images in folder: output-last-run/1-original')
    print()

    print_bar('4.1.')
    print_bar('Webp conversion for all')
    convert_to_webp(starting_folder)
    print("Converted to webp")
    print()

    print_bar('4.2.')
    print_bar('Cropping images to '+str(size_w)+'x'+str(size_h))
    crop_images_logo(starting_folder, size_w, size_h)
    print("Cropped images")
    print()

    print_bar('5.')
    print_bar('To black and white')
    shutil.copytree('output-last-run/1-original', 'output-last-run/2-black-and-white')
    starting_folder = 'output-last-run/2-black-and-white'
    convert_to_black_and_white(starting_folder)
    print("Converted to black and white")
    print()

    print_bar('DONE!')

else:
    print('Invalid mode')
    exit(1)

