import io
import os
import cups
from PIL import Image, ImageDraw, ImageFont
import openai
from google.cloud import vision
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from datetime import datetime
from fontTools.ttLib import TTFont



# Set Google Cloud Vision credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/ziqian/APIKEY.json'

# Instantiate a Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Set your OpenAI API key
openai.api_key = 'XXXXXXXXXXXXXXXXXX'

# Setup
button_pin = 16  # GPIO pin the button is attached to
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
camera = Picamera2()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def take_photo(camera):
    try:
        print("Initializing camera for photo capture...")
        # Assuming 'camera' is a properly initialized Picamera2 object
        config = camera.create_preview_configuration()
        camera.configure(config)
        camera.start()
        time.sleep(2)  # Camera warm-up time

        
        file_name = f"/home/ziqian/Pictures/{timestamp}.jpg"
        print(f"Capturing photo: {file_name}")
        
        # Adjust the capture and save method according to Picamera2 documentation
        camera.capture_file(file_name)
        
        camera.stop()
        print(f"Photo saved: {file_name}")
        return file_name
    except Exception as e:
        print(f"Error taking photo: {e}")
        return None

def image_content(file_name):
    content_list = []
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)
        content_list.append(label.description)

    return content_list
    

def generate_poem(labels):
    messages = [
        {"role": "system", "content": "You are a poetic assistant."},
        {"role": "user", "content": f"Write a haiku about {' and '.join(labels)}."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    if response.choices and response.choices[0].message['content']:
        poem = response.choices[0].message['content'].strip()
    else:
        poem = "No poem generated."
        
    return poem


def create_printable_image(file_name, poem):
    try:
        base_image = Image.open(file_name)
        image_width, image_height = base_image.size
        
        scale_factor = 1  # How much larger to make the text part
        additional_height = 200 * scale_factor  # Scaled up to keep text size larger
        new_image_height = image_height + additional_height // scale_factor
        
        # Create a new, larger image to accommodate both the picture and poem, scaled up for text
        new_image_scaled = Image.new("RGB", (image_width * scale_factor, image_height * scale_factor + additional_height), "black")
        new_image_scaled.paste(base_image.resize((image_width * scale_factor, image_height * scale_factor)), (0, 0))

        # Prepare to draw the text on the scaled image
        draw = ImageDraw.Draw(new_image_scaled)
       
        font = ImageFont.truetype(font='/home/ziqian/Downloads/PTC55F.ttf', size=36)
        # Drawing the text on the scaled section
        text_start_y = image_height * scale_factor + 10  # Scaled starting position
        draw.multiline_text((20 * scale_factor, text_start_y), poem, fill="white", font=font)

        # Resize the image back to a normal size with larger-looking text
        new_image = new_image_scaled.resize((image_width, new_image_height))

         # Save the modified image
        output_file_name = 'image_with_poem.jpg'
        new_image.save(output_file_name)
        print(f"Image saved successfully as {output_file_name}")

        return output_file_name
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
    image_path_with_poem = create_printable_image(file_name, poem)

def print_image(file_path):
    conn = cups.Connection()
    printers = conn.getPrinters()
    default_printer = list(printers.keys())[0]
    print("Default Printer:", default_printer)  # Debugging line
    
    # Print the file
    print_job_id = conn.printFile(default_printer, file_path, "Poem Print", {})
    print("Print Job ID:", print_job_id)  # Debugging line
        
def on_button_press(channel):
    print("Button pressed!")
    file_name = take_photo()
    print(f"Photo taken and saved as {file_name}")
    labels_list = image_content(file_name)
    poem = generate_poem(labels_list)
    print("\nGenerated Poem:\n", poem)
    output_path = create_printable_image(file_name, poem)
    print_image(output_path)
   
   # main loop
try:
    print("Ready for button press.")
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == False:  # Button is pressed (assuming a pull-up resistor configuration)
            print("Button pressed!")
            file_name = take_photo(camera)
            print(f"Photo taken and saved as {file_name}")
            labels_list = image_content(file_name)
            poem = generate_poem(labels_list)
            print("\nGenerated Poem:\n", poem)
            output_path = create_printable_image(file_name, poem)
            print_image(output_path)
            # Wait for the button to be released to avoid multiple captures from one press
            while GPIO.input(button_pin) == False:
                time.sleep(0.1)
        time.sleep(0.1)  # Small delay to reduce CPU usage
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    GPIO.cleanup()
    

def capture_process_print():
    file_name = take_photo(camera)
    if file_name is not None:
        labels_list = image_content(file_name)
        poem = generate_poem(labels_list)
        image_path_with_poem = create_printable_image(file_name, poem)
        if image_path_with_poem:
            print_image(image_path_with_poem)

if __name__ == '__main__':
    try:
        print("Ready for button press.")
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False:  # Button is pressed
                capture_process_print()
                # Wait for button release
                while GPIO.input(button_pin) == False:
                    time.sleep(0.1)
            time.sleep(0.1)  # Reduce CPU usage
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        GPIO.cleanup()