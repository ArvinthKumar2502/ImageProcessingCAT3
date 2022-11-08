# import the necessary packages
from tkinter import *
from tkinter.ttk import Style

from PIL import Image
from PIL import ImageTk
from tkinter import filedialog as tkFileDialog,simpledialog,messagebox
import cv2
import main
import os

def show(result_im=None):
    global panelA, panelB, path
    image = cv2.imread(path)
    if result_im is None:
        result_im = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    edged = cv2.cvtColor(result_im, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    edged = Image.fromarray(edged)
    image = ImageTk.PhotoImage(image)
    edged = ImageTk.PhotoImage(edged)
    if panelA is None or panelB is None:
        panelA = Label(image=image)
        panelA.image = image
        panelA.pack(side="left",ipadx=5, ipady=5,expand=1)
        panelB = Label(image=edged)
        panelB.image = edged
        panelB.pack(side="right",ipadx=5, ipady=5,expand=1)
    else:
        # update the pannels
        panelA.configure(image=image,bg='black')
        panelB.configure(image=edged,bg='black')
        panelA.image = image
        panelB.image = edged

def savefile(edge,colours_):
    edge = cv2.cvtColor(edge, cv2.COLOR_BGR2RGB)
    edge = Image.fromarray(edge)
    # edge = ImageTk.PhotoImage(edge)
    filename = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    edge.save(filename)
    print(filename.name)
    btn4 = Button(root, text="Paint the Point lists", command=lambda: pp(edge,filename.name,colours_),relief=RAISED,bg='white',font=("Arial", 15))
    btn4.pack(side="bottom",fill="both", ipadx="7", ipady="7")
    return filename.name

def pp(i,file,colours_):
    print("painted.... "+file)
    os.system("python paint.py "+file)

def dialog():
    global root, path, btn3,file
    palette = simpledialog.askinteger("Palette size", "What is the palette size?(default=20)[Range : 0-40]",
                                      parent=root,minvalue=0, maxvalue=40)
    if palette is not None:
        palette = palette

    stroke_scale = simpledialog.askinteger("Stroke Scale", "What is stroke scale?(default=0)[Range : 0-100]",
                                     parent=root,
                                     minvalue=0, maxvalue=100)
    if stroke_scale is not None:
        stroke_scale = stroke_scale

    g_s_radius = simpledialog.askinteger("Smoothing Radius", "What is gradient smoothing radius?(default=0)[Range : 0-100]",
                                   parent=root,
                                   minvalue=0, maxvalue=100)
    if g_s_radius is not None:
        g_s_radius = g_s_radius

    l_image_size = simpledialog.askinteger("Image Size", "What is image size?(default=0)[Range : 0-1080]",
                                   parent=root,
                                   minvalue=0, maxvalue=1080)
    if l_image_size is not None:
        l_image_size = l_image_size

    result_im, colours_ = main.point(path,palette,l_image_size,stroke_scale,g_s_radius)
    show(result_im)
    file=""
    btn3 = Button(root, text="Save Pointlist ART", command=lambda: savefile(result_im,colours_),relief=RAISED,bg='white',font=("Arial", 15))
    btn3.pack(side="top",fill="both", ipadx="3", ipady="3")
   
def select_image():
    global path,btn3
    path = tkFileDialog.askopenfilename()

    if len(path) > 0:
        show()
        btn2.pack(side="top", fill="both", expand="yes", padx="10", pady="10")
        btn3.pack_forget()

# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Pointillist Painter")

s = Style()
s.configure('Styled', background='black')

label = Label(
    text="Create a Pointillist Painting by selecting an image and choosing the appropriate Pointillist Values",
    foreground="white",  # Set the text color to white
    background="black",  # Set the background color to black
    font=("Arial", 20)
)
label.pack(fill=X,ipadx=15,ipady=15)

frame2 = Frame(master=root, height=350,bg='black')
frame2.pack(fill=X)

panelA = None
panelB = None
path = None
btn3 = None
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(frame2, text="Choose an image", command=select_image,relief=RAISED,bg='white',font=("Arial", 15),width=22)
btn.pack(side="top", padx="10", pady="10")
btn2 = Button(frame2, text="Select pointillist values", command=dialog,relief=RAISED,bg='white',font=("Arial",15),width=22)
btn2.pack(side="bottom", padx="10", pady="10")
# kick off the GUI
root.mainloop()
