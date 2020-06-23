import os
import random
import tkinter as tk 
from PIL import Image, ImageTk


#global variables
WINDOW_TITLE = "Smart Wardrobe"
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 220
IMG_WIDTH = 220
IMG_HEIGHT = 220

ALL_TOPS = [str("tops/") + file for file in os.listdir("tops/") if not file.startswith('.')]
ALL_BOTTOMS = [str("bottoms/") + file for file in os.listdir("bottoms/") if not file.startswith('.')]
ALL_SHOES = [str("shoes/") + file for file in os.listdir("shoes/") if not file.startswith('.')]

class WardrobeApp():
    def __init__(self, root):
        self.root = root

        #show tops/bottoms/shoes image in window
        self.top_images = ALL_TOPS
        self.bottom_images = ALL_BOTTOMS
        self.shoe_images = ALL_SHOES

        #save single top/bottom/shoe
        self.tops_image_path = self.top_images[0]
        self.bottoms_image_path = self.bottom_images[0]
        self.shoes_image_path = self.shoe_images[0]

        #create and add top image into Frame
        self.tops_frame = tk.Frame(self.root)
        self.top_image_label = self.create_photo(self.tops_image_path, self.tops_frame)

        #create and add bottom image into Frame
        self.bottoms_frame = tk.Frame(self.root)
        self.bottom_image_label = self.create_photo(self.bottoms_image_path, self.bottoms_frame)

        #create and add shoe image into Frame
        self.shoes_frame = tk.Frame(self.root)
        self.shoe_image_label = self.create_photo(self.shoes_image_path, self.shoes_frame)

        #add it to pack
        self.top_image_label.pack(side=tk.TOP)
        self.bottom_image_label.pack(side=tk.TOP)
        self.shoe_image_label.pack(side=tk.TOP)

        #create background
        self.create_background()

    def create_background(self):

        #add title to window and change size
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        #add all buttons
        self.create_buttons()

        #add clothing
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.shoes_frame.pack(fill=tk.BOTH, expand=tk.YES)


    def create_buttons(self):
        top_prev_button = tk.Button(self.tops_frame, text="⬅️", command=self.get_next_top)
        top_prev_button.pack(side=tk.LEFT)

        top_next_button = tk.Button(self.tops_frame, text="➡️", command=self.get_prev_top)
        top_next_button.pack(side=tk.RIGHT)


        bottom_prev_button = tk.Button(self.bottoms_frame, text="⬅️", command=self.get_next_bottom)
        bottom_prev_button.pack(side=tk.LEFT)

        bottom_next_button = tk.Button(self.bottoms_frame, text="➡️", command=self.get_prev_bottom)
        bottom_next_button.pack(side=tk.RIGHT)


        shoe_prev_button = tk.Button(self.shoes_frame, text="⬅️", command=self.get_next_shoe)
        shoe_prev_button.pack(side=tk.LEFT)

        shoe_next_button = tk.Button(self.shoes_frame, text="➡️", command=self.get_prev_shoe)
        shoe_next_button.pack(side=tk.RIGHT)

        create_outfit_button = tk.Button(self.shoes_frame, text="✨ Create Outfit ✨", command=self.create_outfit)
        create_outfit_button.pack(side=tk.BOTTOM)

    #general fn that will allow us to move front and back
    def _get_next_item(self, current_item, category, increment = True):

        #if we know where the curr item index is in a category, then we find the pic before/after it
        item_index = category.index(current_item)
        final_index = len(category)-1
        next_index = 0

        #edge cases
        if increment and item_index == final_index:
            #add the end, and need to up, cycle back to beginning
            next_index = 0
        elif not increment and item_index == 0:
            #cycle back --> end
            next_index = final_index
        else:
            #increments
            increment = 1 if increment else -1
            next_index = item_index + increment

        next_image = category[next_index]

        #reset and update the image based on the next_image path
        if current_item in self.top_images:
            image_label = self.top_image_label
            self.tops_image_path = next_image
        elif current_item in self.bottom_images:
            image_label = self.bottom_image_label
            self.bottoms_image_path = next_image
        else:
            image_label = self.shoe_image_label
            self.shoes_image_path = next_image

        #use update function to change image
        self.update_image(next_image, image_label)

    def get_next_top(self):
        self._get_next_item(self.tops_image_path, self.top_images)

    def get_prev_top(self):
        self._get_next_item(self.tops_image_path, self.top_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.bottoms_image_path, self.bottom_images)

    def get_prev_bottom(self):
        self._get_next_item(self.bottoms_image_path, self.bottom_images, increment=False)

    def get_next_shoe(self):
        self._get_next_item(self.shoes_image_path, self.shoe_images)

    def get_prev_shoe(self):
        self._get_next_item(self.shoes_image_path, self.shoe_images, increment=False)


    def update_image(self, new_image_path, image_label):
        #collect and change into tk photo obj
        image_file = Image.open(new_image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        #update based on provided image label
        image_label.configure(image=tk_photo)

        #tkinter syntax
        image_label.image = tk_photo


    def create_photo(self, image_path, frame):
        image_file = Image.open(image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)
        image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)
        #weird tkinter quirk
        image_label.image = tk_photo
        return image_label

    def create_outfit(self):

        #randomly selects outfits
        new_top_index = random.randint(0,len(self.top_images) - 1)
        new_bottom_index = random.randint(0,len(self.bottom_images) - 1)
        new_shoe_index = random.randint(0,len(self.shoe_images) - 1)

        #add clothes to display
        self.update_image(self.top_images[new_top_index], self.top_image_label)
        self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)
        self.update_image(self.shoe_images[new_shoe_index], self.shoe_image_label)


root = tk.Tk()
app = WardrobeApp(root)
root.mainloop()


