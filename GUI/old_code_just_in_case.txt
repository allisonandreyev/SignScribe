import tkinter as tk
from PIL import Image, ImageTk
import cv2
from time import sleep
import queue


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

def update_hand(hand_queue):
    base_path = r"C:\Users\user\Downloads\Hand_signs"
    if hand_queue in 'abcdefghijklmnopqrstuvwxyz':
        return fr"{base_path}\{hand_queue.upper()}.mp4"
    else:
        return fr"{base_path}\open_palm.mp4"
            

def GUI(text_queue, hand_queue, letter_queue, wordBacklog):

    window = tk.Tk()
    window.geometry('%dx%d+0+0' % (window.winfo_screenwidth(), window.winfo_screenheight()))
    window.title("GUI")

    # Define the exact dimensions and positions for frames
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()

    video_frame = tk.Frame(window)
    video_frame.place(x=0, y=0, width=window_width, height=window_height // 2)

    text_frame = tk.Frame(window, bg='#474747')
    text_frame.place(x=0, y=window_height // 2, width=window_width // 2, height=window_height // 2)

    player = VideoPlayer(video_frame, r"C:\Users\user\Downloads\Hand_signs\O.mp4", window)

    scrollbar = tk.Scrollbar(text_frame, bg="#474747")
    scrollbar.pack(side="right", fill="y")

    textbox = tk.Text(text_frame, bg="#474747", fg="#FFFFFF", wrap="word", yscrollcommand=scrollbar.set, font=('Courier', 18))
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

    Letter_title = tk.Label(Letter_update_frame, bg ="#474747", fg = "#FFFFFF", text="Letter in current read:", font=('Courier', 18))
    Letter_title.place(x = 10, y = 10)

    Letter_show = tk.Text(Letter_update_frame, bg ="#474747", fg = "#FFFFFF", wrap="word", font=('Courier', 120))
    Letter_show.place(x = 250, y = 40, width=200, height=200)
    
    def update_text():
        try:
            new_text = text_queue.get_nowait()
            wordBacklog.clear()
            wordBacklog.extend(new_text.split())
            textbox.delete(1.0, tk.END)
            textbox.insert(tk.END, new_text)

        except queue.Empty:
            pass

        try:
            hand_sign = hand_queue.get_nowait()
            current_word = letter_queue.get_nowait()
            update_hand(hand_sign, current_word)
        except queue.Empty:
            pass

        window.after(100, update_text)

    def update_hand(hand_sign, current_word):
        video_path = f"C:\\Users\\user\\Downloads\\Hand_signs\\{hand_sign}.mp4"
        player.set_path(video_path)
        Letter_show.delete(1.0, tk.END)  # Clear the previous hand_sign
        Letter_show.insert(tk.END, hand_sign.upper())  # Insert the current hand_sign
        highlight_text(current_word)

    def highlight_text(current_word):
        text = textbox.get("1.0", tk.END)
        textbox.tag_remove("highlight", "1.0", tk.END)

        start_index = '1.0'
        while True:
            start_index = textbox.search(current_word, start_index, tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(current_word)}c"
            textbox.tag_add("highlight", start_index, end_index)
            textbox.tag_config("highlight", background="yellow", foreground="black")
            start_index = end_index
            break  # Only highlight the first occurrence

    window.after(100, update_text)
    window.mainloop()


def GUI_APP(text_queue, wordBacklog, hand_queue, letter_queue):
    populate_queue(text_queue, wordBacklog)
    GUI(text_queue, hand_queue, letter_queue, wordBacklog)
