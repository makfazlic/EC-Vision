import math
import os
import face_recognition
import cv2
from PIL import Image, ImageEnhance


def print_bar(s):
        n = 76 - len(s) - 2
        n = n / 2
        if n % 2 == 0:
            n = math.floor(n)
            print('#' * n + ' ' + s + ' ' + '#' * n)
        else:
            n = math.floor(n)
            print('#' * n + ' ' + s + ' ' + '#' * (n + 1))

def files_in_folder(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    return len(files)

def center_faces(folder):
    images = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    count = 0
    for i, image_path in enumerate(images):
        success = False
        reason = ""
        cv_image = cv2.imread(image_path)
        height, width, channels = cv_image.shape
        new_side = min(height, width)
        if cv_image is None:
            success = False
            reason = "Could not read image to cv2"
            # Remove image from folder
            os.remove(image_path)
        else:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                success = False
                reason = "No faces found"
                # Remove image from folder
                os.remove(image_path)
            else:
                top, right, bottom, left = face_locations[0]
                center = (int((left + right) / 2), int((top + bottom) / 2))
                center_x, center_y = center
                if width > height:
                    top = 0
                    bottom = new_side
                    left = min(max(0, center_x - int(new_side / 2)), width - new_side)
                    right = min(left + new_side, width)
                else:
                    left = 0
                    right = new_side
                    top = min(max(0, center_y - int(new_side / 2)), height - new_side)
                    bottom = min(top + new_side, height)
                
                face = cv_image[top:bottom, left:right]

                # write face to file
                cv2.imwrite(image_path, face)
                success = True
                reason = "Face found"
                count += 1
                
            print(f'[{i+1}/{len(images)}] {"✅" if success else "🚫"}: {image_path} ({reason})')
    print(f'Faces found in {count}/{len(images)} images')
    print(f'The output folder is should now contain {files_in_folder(folder)} files')

def resize_image(input_image, size_w, size_h):
    original_image = input_image
    original_image = original_image.convert("RGBA")

    width, height = original_image.size
    aspect_ratio = width / height

    new_width = size_w
    new_height = int(new_width / aspect_ratio)
    if new_height > size_h:
        new_height = size_h
        new_width = int(new_height * aspect_ratio)

    resized_image = original_image.resize((new_width, new_height))

    new_image = Image.new("RGBA", (size_w, size_h), (0, 0, 0, 0))
    new_image.paste(resized_image, ((size_w - new_width) // 2, (size_h - new_height) // 2))

    return new_image

def crop_images(folder, width, height):
    images = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    count = 0
    for i, image_path in enumerate(images):
        success = False
        reason = ""
        cv_image = cv2.imread(image_path)
        if cv_image is None:
            success = False
            reason = "Could not read image to cv2"
            # Remove image from folder
            os.remove(image_path)
        else:
            cv_image = cv2.resize(cv_image, (width, height))
            # write face to file
            cv2.imwrite(image_path, cv_image)
            success = True
            reason = "Face found"
            count += 1

        print(f'[{i+1}/{len(images)}] {"✅" if success else "🚫"}: {image_path} ({reason})')
    print(f'Successfully cropped {count}/{len(images)} images')
    print(f'The output folder is should now contain {files_in_folder(folder)} files')

def crop_images_logo(folder, width, height):
    images = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        image = resize_image(image, width, height)
        image.save(image_path)
        print(f'[{i+1}/{len(images)}] ✅: {image_path}')
    print(f'Successfully cropped {len(images)}/{len(images)} images')
    print(f'The output folder is should now contain {files_in_folder(folder)} files')
            

def convert_to_webp(folder):
    images = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    count = 0
    success = False
    reason = ""
    for i, image_path in enumerate(images):
        try:
            image = Image.open(image_path)
            os.remove(image_path)
            image_path = image_path.replace(image_path.split('.')[-1], 'webp')
            image.save(image_path, 'webp')
            count += 1
            success = True
        except:
            success = False
            reason = "Could not convert"    
        print(f'[{i+1}/{len(images)}] {"Converted to Webp ✅" if success else "Failed to convert 🚫"}: {image_path} ({reason})')
    print(f'Successfully converted {count}/{len(images)} images to webp')
    print(f'The output folder is should now contain {files_in_folder(folder)} files')

def convert_to_black_and_white(folder):
    images = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    count = 0
    success = False
    reason = ""
    for i, image_path in enumerate(images):
        try:
            image = Image.open(image_path)
            image = image.convert('LA')
            os.remove(image_path)
            image.save(image_path)
            count += 1
            success = True
            reason = "success"
        except:
            success = False
            reason = "Could not convert"    
        print(f'[{i+1}/{len(images)}] {"Converted to black and white ✅" if success else "Failed to convert 🚫"}: {image_path} ({reason})')
    print(f'Successfully converted {count}/{len(images)} images to black and white')
    print(f'The output folder is should now contain {files_in_folder(folder)} files')

def calculate_size(folder):
    # calculate the size of the while folder in mega bytes
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    total_size = total_size
    return total_size

def get_diffrent_files(folder_in, folder_out):
    images_in = [filename.split(".")[0] for filename in os.listdir(folder_in) if os.path.isfile(os.path.join(folder_in, filename))]
    images_out = [filename.split(".")[0] for filename in os.listdir(folder_out) if os.path.isfile(os.path.join(folder_out, filename))]
    in_out_not_in_in = [image for image in images_in if image not in images_out]
    return in_out_not_in_in
    