import os
import random


def shuffle_images():
    filename = "shuffle.txt"
    print("Grabbing the next image from {0}".format(filename))
    # Check to see if shuffle.txt exists. If not, let's create it really quick

    if os.path.exists(filename) == False:
        print("Creating {0}".format(filename))
        open(filename, "a").close

    # If the .txt file is blank, it needs to generate a list of images
    if os.lstat(filename).st_size == 0:
        print("{0} is empty. Generating new list".format(filename))
        # Get a list of all images in the images/ directory, then shuffle it.
        filelist = os.listdir("images")
        random.shuffle(filelist)
        with open(filename, "w") as shuffle_file:
            for image in filelist:
                # Validate that the file is in the format NAME.PNG or NAME.JPG
                split = image.split(".")
                if len(split) == 2:
                    if split[1] == "png" or split[1] == "jpg":
                        shuffle_file.write("{0}\n".format(image))

    # Now that we're sure the file exists, return the first line from the file
    # Then dump the rest of the lines back into the file.

    with open(filename, "r") as file_in:
        working_list = file_in.read().splitlines(True)
    read_image = working_list[0].rstrip()
    with open(filename, "w") as file_out:
        file_out.writelines(working_list[1:])

    return read_image


if __name__ == "__main__":
    shuffle_images()
