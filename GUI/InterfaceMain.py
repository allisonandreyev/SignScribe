import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from time import sleep
import queue

def write_to_file(tk_entry, variable, value_type):
    try:
        value = tk_entry.get()
        
        # Convert the value to the appropriate type
        if value_type == 'float':
            value = float(value)
        elif value_type == 'bool':
            value = value.lower() in ['true', '1', 'yes']
        
        # Read the current content of config.txt
        with open(r'/home/signscribe/Downloads/SignScribe-master/Code Files/Config.txt', "r") as file:
            lines = file.readlines()
        
        # Update the value
        for i, line in enumerate(lines):
            if line.startswith(variable):
                if value_type == 'string':
                    lines[i] = f'{variable} = "{value}"\n'
                else:
                    lines[i] = f'{variable} = "{value}"\n'
                break
        else:
            # If the variable is not found, append it
            if value_type == 'string':
                lines.append(f'{variable} = "{value}"\n')
            else:
                lines.append(f'{variable} = "{value}"\n')
        
        # Write the updated content back to config.txt
        with open(r'/home/signscribe/Downloads/SignScribe-master/Code Files/Config.txt', "w") as file:
            file.writelines(lines)
        
        messagebox.showinfo("Success", f'{variable} value written to config.txt')
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid value")

class VideoPlayer:
    def __init__(self, parent_frame, video_path, window):
        self.parent_frame = parent_frame
        self.window = window
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.label = tk.Label(parent_frame)
        self.label.place(x=0, y=0, width=window.winfo_screenwidth()//2, height=window.winfo_screenheight()//2)

        self.playing = True
        self.update_frame()

    def set_path(self, path):
        self.video_path = path
        self.cap.release()  # Release the previous video capture
        self.cap = cv2.VideoCapture(self.video_path)  # Open the new video
        self.playing = True  # Reset playing state
        self.update_frame()

    def update_frame(self):
        if not self.playing:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            self.parent_frame.after(10, self.update_frame)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playing = False  # Stop the video from looping

    def stop(self):
        self.playing = False


def populate_queue(text_queue, wordBacklog):
    for _ in range(10):
        formatted_text = format_text(wordBacklog)
        text_queue.put(formatted_text)

def format_text(wordBacklog):
    lines = []
    for i in range(0, len(wordBacklog), 5):
        line = ' '.join(wordBacklog[i:i+5])
        lines.append(line)
    updated_text = '\n'.join(lines)
    return updated_text

def update_hand_letter(hand_queue):
    match hand_queue:
        case 'a':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/A.mp4"
        case 'b':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/B.mp4"
        case 'c':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/C.mp4"    
        case 'd':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/D.mp4"
        case 'e':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/E.mp4"
        case 'f':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/F.mp4"
        case 'g':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/G.mp4"
        case 'h':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/H.mp4"
        case 'i':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/I.mp4"
        case 'j':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/J.mp4"
        case 'k':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/K.mp4"
        case 'l':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/L.mp4"
        case 'm':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/M.mp4"
        case 'n':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/N.mp4"
        case 'o':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/O.mp4"
        case 'p':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/P.mp4"
        case 'q':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/Q.mp4"
        case 'r':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/R.mp4"
        case 's':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/S.mp4"
        case 't':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/T.mp4"
        case 'u':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/U.mp4"
        case 'v':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/V.mp4"
        case 'w':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/W.mp4"
        case 'x':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/X.mp4"
        case 'y':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/Y.mp4"
        case 'z':
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/Z.mp4"
        case _:
            return r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/open_palm.mp4"
            
def set_config_variables(lettersPause, wordPause, exitWord, autoSave, autoLaunch):
    write_to_file(lettersPause, "lettersPause", "float")
    write_to_file(wordPause, "wordsPause", "float")
    write_to_file(exitWord, "exitWord", "string")
    write_to_file(autoSave, "autoSave", "bool")
    write_to_file(autoLaunch, "autoLaunch", "bool")

'''
GUI function is the function responsible for drawing and updating all of the visual elements on the screen
'''
def GUI(text_queue, hand_queue):

    #this is where the application window is made
    #window - the variable that refers to the application window itself
    window = tk.Tk()
    #this sets the dimensions of the application window to the native resolution of whatever device it's on
    window.geometry('%dx%d+0+0' % (window.winfo_screenwidth(), window.winfo_screenheight()))
    #this sets what text is displayed in the top left corner of the application window
    window.title("GUI")

    '''
    the dimension of the window is stored in two variables
    this is done so that other elements being drawn on the screen can base their dimension and placement dynamically off the size of the window
    '''
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()

    '''
    A frame in tkinter is a box element used to organize other elements on the screen by acting as a the associated parent
    here video_frame is the element responsible for containing the 3D animations of the hand signing within the area and placement specified by .place method
    '''
    video_frame = tk.Frame(window)
    video_frame.place(x=0, y=0, width=window_width, height=window_height // 2)

    #here text_frame is the element responsible for containing the real time display of wordBacklog within the area and placement specified by .place method
    text_frame = tk.Frame(window, bg='#474747')
    text_frame.place(x=0, y=window_height // 2, width=window_width // 2, height=window_height // 2)

    '''
    initializes the mp4 player functionality that runs each 3D animation
    this is where the 3D animations for the hand are played out on the screen
    first argument of constructor sets parent
    second argument of constructor sets directory path to mp4 being played
        NOTE: mp4s must be VERY short in length, any slower than current mp4s and it WILL NOT keep up with bionic hand
    third argument of constructor is specifying the application window this functionality parented to
    '''
    player = VideoPlayer(video_frame, r"/home/signscribe/Downloads/SignScribe-master/Hand_signs/open_palm.mp4", window)

    '''
    this is the scrollbar at the right-most side of the text_frame for when wordBacklog appends beyond the space of text_frame on screen
    '''
    scrollbar = tk.Scrollbar(text_frame, bg="#474747")
    scrollbar.pack(side="right", fill="y")

    '''
    textbox is the functionality that displays the contents of wordBacklog real time
    here it is being defined, parented under text_frame, and configured with the previously defined scrollbar
    '''
    textbox = tk.Text(text_frame, bg="#474747", fg="#FFFFFF", wrap="word", yscrollcommand=scrollbar.set, font=('Bell Gothic Std Black', 18))
    textbox.pack(fill="both", expand=True)
    scrollbar.config(command=textbox.yview, bg="#474747")
    
    # Define the UI frame
    UI_frame = tk.Frame(window, bg='#474747')
    UI_frame.place(x=window_width/2, y=0, width=window_width // 2, height=window_height)

    # Define the dimensions for Letter_update_frame
    frame_width = (window_width // 2) - (window_width // 30)
    frame_height = (window_height // 3) - (window_height // 30)
    
    # Calculate the x position to center Letter_update_frame in UI_frame
    x_position = ((window_width // 2) - frame_width) // 2

    # Define the Letter_update_frame
    Letter_update_frame = tk.Frame(UI_frame, bg="#474747")
    Letter_update_frame.place(
        x=x_position,
        y=(window_height // 30),
        width=frame_width,
        height=frame_height
    )

    # Add a border to visualize the frame
    Letter_update_frame.config(highlightbackground="white", highlightthickness=4)

    Letter_title = tk.Label(Letter_update_frame, bg ="#474747", fg = "#FFFFFF", text="Letter in current read:", font=('Bell Gothic Std Black', 18))
    Letter_title.place(x = 10, y = 10)

    Letter_show = tk.Text(Letter_update_frame, bg ="#474747", fg = "#FFFFFF", wrap="word", font=('Courier', 120))
    Letter_show.place(x = 250, y = 40, width=200, height=200)
    
    Speed_frame = tk.Frame(UI_frame, bg="#474747")
    Speed_frame.place(
        x=x_position,
        y= (2 * (window_height // 30)) + frame_height,
        width=frame_width,
        height=frame_height
    )
    
    Speed_frame.config(highlightbackground="white", highlightthickness=4)

    Speed_title = tk.Label(Speed_frame, bg ="#474747", fg = "#FFFFFF", text="Config Settings:", font=('Bell Gothic Std Black', 18))
    Speed_title.place(x = 10, y = 10)

        # Letter Pause
    letter_pause_label = tk.Label(Speed_frame, text="Letter Pause", bg ="#474747", fg = "#FFFFFF", font=('Bell Gothic Std Black', 11))
    letter_pause_label.place(x=frame_width/6, y=80)  # Place label above the entry
    letter_pause_control = tk.Entry(Speed_frame)
    letter_pause_control.place(x=frame_width/6, y=100)

    # Word Pause
    word_pause_label = tk.Label(Speed_frame, text="Word Pause", bg ="#474747", fg = "#FFFFFF", font=('Bell Gothic Std Black', 11))
    word_pause_label.place(x=frame_width/6, y=130)  # Place label above the entry
    word_pause_control = tk.Entry(Speed_frame)
    word_pause_control.place(x=frame_width/6, y=150)

    # Exit Word
    exit_word_label = tk.Label(Speed_frame, text="Exit Word", bg ="#474747", fg = "#FFFFFF", font=('Bell Gothic Std Black', 11))
    exit_word_label.place(x=frame_width/6, y=180)  # Place label above the entry
    exit_word_control = tk.Entry(Speed_frame)
    exit_word_control.place(x=frame_width/6, y=200)

    # Auto Save
    auto_save_label = tk.Label(Speed_frame, text="Auto Save", bg ="#474747", fg = "#FFFFFF", font=('Bell Gothic Std Black', 11))
    auto_save_label.place(x=4 * (frame_width/6), y=80)  # Place label above the entry
    auto_save_control = tk.Entry(Speed_frame)
    auto_save_control.place(x=4 * (frame_width/6), y=100)

    # Auto Launch GUI
    auto_launch_label = tk.Label(Speed_frame, text="Auto Launch GUI", bg ="#474747", fg = "#FFFFFF", font=('Bell Gothic Std Black', 11))
    auto_launch_label.place(x=4 * (frame_width/6), y=130)  # Place label above the entry
    auto_launch_control = tk.Entry(Speed_frame)
    auto_launch_control.place(x=4 * (frame_width/6), y=150)


    Set_speed = tk.Button(Speed_frame, text="Set variables", command=lambda: set_config_variables(letter_pause_control, word_pause_control, exit_word_control, auto_save_control, auto_launch_control))
    Set_speed.place(x = frame_height, y = 250)

    def update_text():
        try:
            new_text = text_queue.get_nowait()
            textbox.delete(1.0, tk.END)
            textbox.insert(tk.END, new_text)
        except queue.Empty:
            pass
        
        try:
            hand_sign = hand_queue.get_nowait()
            update_hand(hand_sign)
        except queue.Empty:
            pass

        window.after(100, update_text)

    def update_hand(hand_sign):
        video_path = update_hand_letter(hand_sign)
        player.set_path(video_path)
        Letter_show.delete(1.0, tk.END)  # Clear the previous hand_sign
        Letter_show.insert(tk.END, hand_sign.upper())  # Insert the current hand_sign

    window.after(100, update_text)
    window.mainloop()

def GUI_APP(text_queue, wordBacklog, hand_queue):
    populate_queue(text_queue, wordBacklog)
    GUI(text_queue, hand_queue)
