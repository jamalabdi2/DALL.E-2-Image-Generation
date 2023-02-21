
#!pip install openai

"""**Generated images can have a size of 256x256, 512x512, or 1024x1024 pixels**

**User can request 1-10 images at a time using the n parameter.**
"""

import openai
import cv2
import requests
import urllib.request
import matplotlib.pyplot as plt

def generate_images(api_key_file, image_description, n_images=1, image_size='512x512'):
    """
    Generates one or more images using OpenAI's DALL·E 2 API and displays them.

    Parameters:
    - api_key_file (str): Path to a file containing the OpenAI API key.
    - image_description (str): A textual description of the image to be generated.
    - n_images (int, optional): The number of images to generate (default: 1).
    - image_size (str, optional): The size of the images to generate. Must be one of '256x256', '512x512', or '1024x1024' (default: '512x512').

    Returns: None
    """

    # Read OpenAI API key from file
    with open(api_key_file, 'r') as f:
        api_key = f.read().strip()

    # Set OpenAI API key
    openai.api_key = api_key

    # Define constants
    IMAGE_SIZES = ['256x256', '512x512', '1024x1024']
    DEFAULT_IMAGE_SIZE = '512x512'
    MIN_IMAGES = 1
    MAX_IMAGES = 10

    # Prompt the user to enter the number of images to generate
    while True:
        try:
            n_images = int(input(f'How many images do you want to generate? (Enter a number between {MIN_IMAGES} and {MAX_IMAGES}): '))
            if n_images < MIN_IMAGES or n_images > MAX_IMAGES:
                raise ValueError
            break
        except ValueError:
            print(f'Invalid input. Please enter a number between {MIN_IMAGES} and {MAX_IMAGES}.')

# Prompt the user to select the size of the image to generate
    while True:
        try:
            image_size = input(f'What size do you want the image(s) to be? ({", ".join(IMAGE_SIZES)}) [default: {DEFAULT_IMAGE_SIZE}] ')
            if not image_size:
                image_size = DEFAULT_IMAGE_SIZE
                break
            if image_size not in IMAGE_SIZES:
              raise ValueError
            break
        except ValueError:
            print(f'Invalid input. Please enter one of the following sizes: {", ".join(IMAGE_SIZES)}')

    # Parse image_size input
    image_size = image_size.strip('[]') # Remove any brackets around the input
    image_size = image_size.replace(' ', '') # Remove any spaces in the input

    # Validate inputs
    if n_images < MIN_IMAGES or n_images > MAX_IMAGES:
        raise ValueError(f"Invalid input for n_images. Please enter a number between {MIN_IMAGES} and {MAX_IMAGES}.")

    if image_size not in IMAGE_SIZES:
        raise ValueError(f"Invalid input for image_size. Please enter one of the following sizes: {', '.join(IMAGE_SIZES)}")

    # Generate images using OpenAI API
    img_response = openai.Image.create(prompt=image_description, n=n_images, size=image_size)

    # Get image URLs from API response and download them
    for i, image_data in enumerate(img_response['data']):
        img_url = image_data['url']
        filename = f'image_{i+1}.png'
        urllib.request.urlretrieve(img_url, filename)
        img = cv2.imread(filename)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()

api_key_file = '/content/api_key.txt'
image_description = input('Input the image description: ')
generate_images(api_key_file,image_description, n_images=1, image_size='512x512')