import json
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import qrcode
import time

with open('attended.json', 'r') as json_file:  # JSON TO BE READ, PARTICIPANTS IS THE ARRAY HOLDING ALL PARTICIPANTS' DETAILS
    data = json.load(json_file)

list_of_names = []
list_of_pos = []
list_of_rollno = []
# participant [{stud 1}, {stud 2}] -> structure of the JSON
for participant in data['participants']:  # List of data to be used from the JSON, participant is the main class, under which there is Name, Position, Roll #, TO BE CHANGED DEPENDING ON THE JSON
    list_of_names.append(participant['Name'])
    #list_of_pos.append(participant['Position'])
    list_of_rollno.append(participant['Roll #'])

def delete_old_data():
    for i in os.listdir("temp-imgs/"):  # deleting old created data
        os.remove(os.path.join("temp-imgs", i))

def cleanup_data():  # Reinitializing arrays.
    global list_of_names, list_of_events
    list_of_names = []
    list_of_events = []
    list_of_rollno = []

    for participant in data['participants']:
        list_of_names.append(participant['Name'])
        #list_of_pos.append(participant['Position'])
        list_of_rollno.append(participant['Roll #'])

def generate_certificates():
    pos = 0
    for index, (name,roll) in enumerate(zip(list_of_names,list_of_rollno)): # add in the () to add more stuff to the certificate add pos, list_of_pos for winners
        #cert_1 = cv2.imread("temp-1.jpg")  THESE ARE FOR WINNERS LIST , add Position: 1,2,3 in json to use this
        #cert_2 = cv2.imread("temp-2.jpg")
        #cert_3 = cv2.imread("temp-3.jpg")
        cert_p = cv2.imread("temp-p.jpg")   # CAN use Position for this also, by saying participant/organizer cert_p -> participant, cert_c -> organizer
        cert_c = cv2.imread("temp-c.jpg")

        if (pos == "1"): #Conditions for winners
            #im_1 = Image.fromarray(cert_1)
            draw_1 = ImageDraw.Draw(im_1)
        
        elif (pos == "2"):
            #im_1 = Image.fromarray(cert_2)
            draw_1 = ImageDraw.Draw(im_1)
        
        elif (pos == "3") :
            #im_1 = Image.fromarray(cert_3)
            draw_1 = ImageDraw.Draw(im_1)
        else: # default participants or Contribs, can be another ifelse, but I usually do it one at a time so i change
            im_1 = Image.fromarray(cert_c)
            #im_1 = Image.fromarray(cert_p)
            draw_1 = ImageDraw.Draw(im_1)

        pinyon = ImageFont.truetype("Pinyon.ttf",96) # FONT currently used is called Pinyon, ensure the fonts are of TrueType, experiment with size
        W,H = 1365,781 #dimensions of the certificate
        w,h = draw_1.textsize(name,font=pinyon) #size of each person's name calculated to center in the dash ___

        draw_1.text((((W-w)/2),752),name,(0,0,0),font=pinyon) # copy this and change name to anything to use the different arrays !!!color!!! 000 is current color, location, font.
        #752 is the height to place the name (TIP of the letters' height) 1365 is max length of where the name can be 
        # it does 1365 - 20px(for my name example) -> 1345/2 -> 673 px will be where the start of my name will be
        result_o = np.array(im_1)

        cv2.imwrite("temp-imgs/{}.jpg".format(roll), result_o) # store the pngs temporarily to convert
        print("Processing {} / {}".format(index + 1,len(list_of_names)))
      


def convert_images_to_pdfs(image_folder, pdf_destination): #converting everything in the final_cert folder to pdf with a name and a progress message
    images = [f for f in os.listdir(image_folder) if f.endswith(".jpg") or f.endswith(".png")]
    
    if not images:
        print("No images found in the specified folder.")
        return
    
    for image in images:
        image_path = os.path.join(image_folder, image)
        pdf_path = os.path.join(pdf_destination, f"{os.path.splitext(image)[0]}.pdf")
        
        with Image.open(image_path) as img:
            img.save(pdf_path, "PDF")
        
        print(f"Image '{image}' saved as PDF: {pdf_path}")

def generate_qr_codes():
    qr_folder = "qr-codes"
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    for rollno in list_of_rollno:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        qr.add_data(f"insert link here") # Change link for QR to lead to
        qr.make(fit=True)

        img = qr.make_image(fill_color=(94, 23, 235), back_color=(255,255,255))  # Edit colors of QR

        qr_path = os.path.join(qr_folder, f"{rollno}.png") #Location of QR
        img.save(qr_path)

        print(f"QR Code for {rollno} saved: {qr_path}") # Progress messages in console

def place_qr():
    qr_folder = "qr-codes"
    image_folder = "temp-imgs"

    for rollno in list_of_rollno:
        im1 = os.path.join(image_folder, f"{rollno}.jpg") #Temp image created in the generate_certificate() function
        im2 = os.path.join(qr_folder, f"{rollno}.png") #QR filename (uses the rollno from initial list_of_rollno array)
        im1 = Image.open(im1)
        im2 = Image.open(im2)

        back_im = im1.copy()
        back_im.paste(im2, (1200, 365)) #Location to paste the GENERATED QRs

        final_path = os.path.join("final_cert", f"{rollno}.png") #Change for Filename

        back_im.save(final_path)

        ''' for creation timestamp.
        creation_time = os.path.getctime(final_path)
        creation_datetime = time.ctime(creation_time)
        watermark_text = f"This is a valid certificate as created on {creation_datetime} by {name}" #sets time at which this script was run, and creates a grey watermark on 
        
        # the certificate,  this was only displayed during x, {sample_link} for example.


        img = Image.open(final_path).convert("RGBA")
        # Define a threshold value for brightness
        threshold = 128  # You can adjust this threshold as needed
        pixels = list(img.getdata())

        # Initialize counters for light and dark colors
        light_count = 0
        dark_count = 0


        for pixel in pixels:
            # Calculate brightness (average of RGB values)
            brightness = sum(pixel) / 3  # Assuming RGB channels have equal weight

            # Check if the pixel is light or dark based on the threshold
            if brightness > threshold:
                light_count += 1
            else:
                dark_count += 1

        if dark_count>light_count:
            txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
        else:
            txt = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt)
        monospace = font = ImageFont.truetype("Alegreya.ttf",32)

        if dark_count>light_count:
            draw.text((125,840), watermark_text, font=monospace, fill=(255, 255, 255, 64))
        else:
            draw.text((125,840), watermark_text, font=monospace, fill=(0, 0, 0, 64))
        
        out = Image.alpha_composite(img, txt).convert('RGB')
        
        final_path = os.path.join("final_cert", f"{rollno}P.png") #change

        out.save(final_path)
        '''
    



def main():
    #delete_old_data()
    cleanup_data() # clearing the arrays.
    generate_certificates() # creates certifs and places in temp-imgs folder, which is then accessed by place_qr to place qr and save into final_cert,
    # if not using QR, change save location from "temp-imgs to final_cert in generate_certificates()"

    image_folder = "final_cert" # folder with the temporary images of the certificates -> after qr placement
    pdf_destination = "cert-pdfs" # folder for the destination for the pdfs

    generate_qr_codes() #generates QR

    place_qr() #places the generated QRs

    #convert_images_to_pdfs(image_folder, pdf_destination)

    # General Note, to Select the locaiton of placement of details, use paint to find the coordinates,  it shows the coordinates in the bottom of the screen for wherever the
    # mouse is.

if __name__ == '__main__':
    main()


