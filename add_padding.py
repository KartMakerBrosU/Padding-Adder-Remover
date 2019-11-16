# TODO: error checknig for prereqs... use bash file to download?
import cv2
import numpy as np
import sys

# TODO:
# O Some sort of shell script to use pip to get the necessary libraries.
# O WINDOWS???
# O Handle input errors. -> Obviously check for more.

# Gets the ball rolling
def main(PADDING_PIXELS, SIDE_LENGTH, FILE_NAME, NEW_FILE_NAME):

	# open up an image. Extra arg preserves alpha channel.
	original_img = cv2.imread(FILE_NAME, cv2.IMREAD_UNCHANGED)

	# If FileNotFound then original_img will be None
	if not original_img.any():
		bail("Original image file not found. Check the provided path.")

	# Split the image into 2D list. The images in this list have padding.
	images = split_image(SIDE_LENGTH, PADDING_PIXELS, original_img)

	# Finally, recombine all the smaller images and save the resultant image.
	recombine(images, NEW_FILE_NAME)


# Splits the given image into individual images. Saves in 2D array.
def split_image(SIDE_LENGTH, PADDING_PIXELS, original_img):

	# If padding pixels is negative (reduction) then need to add the pixels of padding
	# to the side lengths.
	if PADDING_PIXELS < 0:
		SIDE_LENGTH += 2 * abs(PADDING_PIXELS)

	# get height and width
	height = original_img.shape[0]
	width = original_img.shape[1]

	# height and width should be cleanly divisible by SIDE_LENGTH.
	# If not, most likely was a user input error for SIDE_LENGTH.
	# Either that or image isnt correct... but who knows figure it out later.
	#assert height % SIDE_LENGTH == 0 and width % SIDE_LENGTH == 0

	# Iterate by columns first.
	# Temporarily store images in 2D array and use to reconstruct image later.
	images = []
	for i in range(0, width, SIDE_LENGTH):
		row = []
		for j in range(0, height, SIDE_LENGTH):

			# slice the image
			temp_img = original_img[j:j+SIDE_LENGTH, i:i+SIDE_LENGTH]

			# Now apply the padding if padding pixels is positive (enlargement).
			if PADDING_PIXELS > 0:
				temp_img = cv2.copyMakeBorder(temp_img,PADDING_PIXELS,PADDING_PIXELS,PADDING_PIXELS,
							PADDING_PIXELS,cv2.BORDER_REPLICATE)
			
			# If its negative just slice it to the required pixels.
			elif PADDING_PIXELS < 0:
				temp_img = temp_img[abs(PADDING_PIXELS):(SIDE_LENGTH - abs(PADDING_PIXELS)), 
									abs(PADDING_PIXELS):(SIDE_LENGTH - abs(PADDING_PIXELS))]

			row.append(temp_img)

		images.append(row)
	
	return images


# Takes split image 2D array and recreates our new image with new dimensions
def recombine(images, filename):
	# Objects in images are all cv2 images (or actually maybe numpy arrays.)
	# So maybe we can just concatenate all rows and all columns?
	rows = []
	for column in images:
		im_vertical = cv2.vconcat(column)
		rows.append(im_vertical)
	
	# Now concatenate all the rows vertically
	result = cv2.hconcat(rows)
	cv2.imwrite(filename, result)


# Get the inputs from the user.
def prompt_user():

	print("Mario Maker texture file padding adder/reducer.")
	print("Alright just follow the prompts.")

	print("\n\nEnter the number of pixels to add.")
	print("A positive number will add a buffer.")
	print("A negative number will remove a buffer.")
	try:
		PADDING_PIXELS = int(input("Number of padding pixels: "))
	except ValueError:
		bail("Nope. Try again. This needs to be an integer.")

	print("\n\nEnter the side length of each INDIVIDUAL image.")
	print("Note: This assumes the images are square!")
	try:
		SIDE_LENGTH = int(input("Side length: "))
	except ValueError:
		bail("Nope. Try again. This needs to be an integer.")

	print("\n\nEnter the file name (or path to file) of image to be manipulated.")
	FILE_NAME = input("Path to image: ")

	print("\n\nEnter the file name that you wish to save the image to.")
	NEW_FILE_NAME = input("Image destination: ")

	main(PADDING_PIXELS, SIDE_LENGTH, FILE_NAME, NEW_FILE_NAME)


def bail(message):
	print("\n" + message)
	sys.exit()


prompt_user()
