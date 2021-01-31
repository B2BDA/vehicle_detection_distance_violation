from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2
from vehicle_detection_app import DetectVehicle
vd = DetectVehicle()

class videoGUI:

    def __init__(self, window, window_title):

        self.window = window
        self.window.title(window_title)

        top_frame = Frame(self.window)
        top_frame.pack(side=TOP, pady=5)

        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, pady=5)

        self.pause = False   # Parameter that controls pause button

        self.canvas = Canvas(top_frame)
        self.canvas.pack()

        # Select Button
        self.btn_select=Button(bottom_frame, text="Select video file", width=15, command=self.open_file)
        self.btn_select.grid(row=0, column=0)
        
        # Play Button
        self.btn_play=Button(bottom_frame, text="Process Video", width=15, command=self.process)
        self.btn_play.grid(row=0, column=1)
        
        # Select Button
        self.btn_select=Button(bottom_frame, text="Select processed video file", width=20, command=self.open_processed_file)
        self.btn_select.grid(row=0, column=2)

        # Play Button
        self.btn_play=Button(bottom_frame, text="Play", width=15, command=self.play_video)
        self.btn_play.grid(row=0, column=3)

        # Pause Button
        self.btn_pause=Button(bottom_frame, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=0, column=4)

        # Resume Button
        self.btn_resume=Button(bottom_frame, text="resume", width=15, command=self.resume_video)
        self.btn_resume.grid(row=0, column=5)
    

        self.delay = 15   # ms

        self.window.mainloop()


    def open_file(self):

        self.pause = False

        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),
                                                                                         ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        print(self.filename)

        # Open the video file
        self.cap = cv2.VideoCapture(self.filename)

        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas.config(width = self.width, height = self.height)
        
    def process(self):
        vd.process_video(self.filename)
        # self.cap = cv2.VideoCapture(vd.args["output"])
        
    def open_processed_file(self):

        self.pause1 = False
        self.filename1 = vd.args["output"]
        print(self.filename1)

        # Open the video file
        self.cap1 = cv2.VideoCapture(self.filename1)

        self.width1 = self.cap1.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height1 = self.cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas.config(width = self.width1, height = self.height1)

    def get_frame(self):   # get only one frame
        # self.cap = cv2.VideoCapture(vd.args["output"])
        
        try:

            if self.cap1.isOpened():
                ret, frame = self.cap1.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        except:
            messagebox.showerror(title='Video file not found', message='Please select a video file.')
            sys.exit()


    def play_video(self):

        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        if not self.pause:
            self.window.after(self.delay, self.play_video)


    def pause_video(self):
        self.pause = True

#Addition
    def resume_video(self):
        self.pause=False
        self.play_video()


    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

# ##### End Class #####


# Create a window and pass it to videoGUI Class
videoGUI(Tk(), "Traffic")