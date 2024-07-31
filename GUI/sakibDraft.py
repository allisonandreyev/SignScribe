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
        self.label.place(x=0, y=0, width=window.winfo_screenwidth() // 2, height=window.winfo_screenheight() // 2)

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
            frame = cv2.resize(frame, (self.label.winfo_width(), self.label.winfo_height()))  # Resize the frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            self.parent_frame.after(30, self.update_frame)  # Process every 30 ms (approx 33 FPS)
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
    match hand_queue:
        case 'a':
            return r"C:\Users\user\Downloads\Hand_signs\A.mp4"
        case 'b':
            return r"C:\Users\user\Downloads\Hand_signs\B.mp4"
        case 'c':
            return r"C:\Users\user\Downloads\Hand_signs\C.mp4"    
        case 'd':
            return r"C:\Users\user\Downloads\Hand_signs\D.mp4"
        case 'e':
            return r"C:\Users\user\Downloads\Hand_signs\E.mp4"
        case 'f':
            return r"C:\Users\user\Downloads\Hand_signs\F.mp4"
        case 'g':
            return r"C:\Users\user\Downloads\Hand_signs\E.mp4"
        case 'h':
            return r"C:\Users\user\Downloads\Hand_signs\H.mp4"
        case 'i':
            return r"C:\Users\user\Downloads\Hand_signs\I.mp4"
        case 'j':
            return r"C:\Users\user\Downloads\Hand_signs\J.mp4"
        case 'k':
            return r"C:\Users\user\Downloads\Hand_signs\K.mp4"
        case 'l':
            return r"C:\Users\user\Downloads\Hand_signs\L.mp4"
        case 'm':
            return r"C:\Users\user\Downloads\Hand_signs\M.mp4"
        case 'n':
            return r"C:\Users\user\Downloads\Hand_signs\N.mp4"
        case 'o':
            return r"C:\Users\user\Downloads\Hand_signs\O.mp4"
        case 'p':
            return r"C:\Users\user\Downloads\Hand_signs\P.mp4"
        case 'q':
            return r"C:\Users\user\Downloads\Hand_signs\Q.mp4"
        case 'r':
            return r"C:\Users\user\Downloads\Hand_signs\R.mp4"
        case 's':
            return r"C:\Users\user\Downloads\Hand_signs\A.mp4"
        case 't':
            return r"C:\Users\user\Downloads\Hand_signs\T.mp4"
        case 'u':
            return r"C:\Users\user\Downloads\Hand_signs\U.mp4"
        case 'v':
            return r"C:\Users\user\Downloads\Hand_signs\V.mp4"
        case 'w':
            return r"C:\Users\user\Downloads\Hand_signs\W.mp4"
        case 'x':
            return r"C:\Users\user\Downloads\Hand_signs\X.mp4"
        case 'y':
            return r"C:\Users\user\Downloads\Hand_signs\Y.mp4"
        case 'z':
            return r"C:\Users\user\Downloads\Hand_signs\Z.mp4"
        case _:
            return r"C:\Users\user\Downloads\Hand_signs\open_palm.mp4"
            

def GUI(text_queue, hand_queue):

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
    player.set_path(r"C:\Users\user\Downloads\Hand_signs\A.mp4")

    scrollbar = tk.Scrollbar(text_frame, bg="#474747")
    scrollbar.pack(side="right", fill="y")

    textbox = tk.Text(text_frame, bg="#474747", fg="#FFFFFF", wrap="word", yscrollcommand=scrollbar.set, font=('monospace', 18))
    textbox.pack(fill="both", expand=True)
    scrollbar.config(command=textbox.yview, bg="#474747")

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
        video_path = f"C:\\Users\\user\\Downloads\\Hand_signs\\{hand_sign}.mp4"
        player.set_path(video_path)
        highlight_text(hand_sign)

    def highlight_text(hand_sign):
        text = textbox.get("1.0", tk.END)
        index = text.lower().find(hand_sign.lower())
        if index != -1:
            textbox.tag_remove("highlight", "1.0", tk.END)
            textbox.tag_add("highlight", f"1.{index}", f"1.{index+1}")
            textbox.tag_config("highlight", background="yellow", foreground="black")

    window.after(100, update_text)
    window.mainloop()

def GUI_APP(text_queue, wordBacklog, hand_queue):
    populate_queue(text_queue, wordBacklog)
    GUI(text_queue, hand_queue)
