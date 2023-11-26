from datetime import timedelta
from tkinter import *
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from modules.my_attributes import myAttributes

from modules.playerFunc import playerFunctions


class videoPlayer():

    def __init__(self, boss):
        self.boss = boss
        self.pf = playerFunctions()
        self.file_path = None

        self.slider1 = None
        self.slider2 = None

        # print("hii")
        self.right_frame = Frame(
            self.boss.my_frame1,  width=(self.boss.width/3)*2,  height=400, borderwidth="4", relief="groove")
        # self.right_frame.grid(row=0,  column=1,  padx=10,
        #                       pady=5, columnspan=5, rowspan=5)
        self.right_frame.grid(row=0,  column=1,  padx=0, pady=2)

        # self.vid_player = TkinterVideo(scaled=True, master=self.right_frame)
        # # self.vid_player.pack(expand=True, fill="both")
        # self.vid_player.grid(row=0, column=0)

        self.preview()
        self.controls_bar()
        self.pf.setVars(self.vid_player, self.play_pause_btn,
                        self.skip_plus_5sec, self.start_time, self.progress_value, self.progress_slider, self.end_time)

    def controls_bar(self):
        self.control_bar = Frame(
            self.right_frame, width=(self.boss.width/3)*2, height=50)
        self.control_bar.grid(row=1, column=0, padx=0, pady=0)
        # self.control_bar.pack()

        self.play_pause_btn = Button(
            self.control_bar, text=myAttributes.play, command=lambda: self.pf.play_pause())
        self.play_pause_btn.grid(row=0, column=0, padx=5)

        self.skip_plus_5sec = Button(self.control_bar, text=myAttributes.skipm5,
                                     command=lambda: self.pf.skip(self.vid_player, self.progress_slider, self.progress_value, -5))
        self.skip_plus_5sec.grid(row=0, column=1, padx=5)

        self.start_time = Label(
            self.control_bar, text=str(timedelta(seconds=0)))
        self.start_time.grid(row=0, column=2, padx=5)

        self.slider_frame = Frame(
            self.control_bar, width=400)
        self.progress_value = IntVar(self.slider_frame)
        self.progress_slider = Scale(self.slider_frame, variable=self.progress_value, showvalue=False,
                                     from_=0, to=0, orient="horizontal", command=self.pf.seek, length=400)
        # self.progress_slider.bind("<ButtonRelease-1>", self.seek)
        # self.progress_slider.bind("<ButtonRelease-1>", self.seek)
        # self.progress_slider.pack(side="left", fill="x", expand=True)
        self.progress_slider.grid(row=0, column=0)
        self.slider_frame.grid(row=0, column=3, rowspan=3, padx=10)

        self.end_time = Label(self.control_bar, text=str(timedelta(seconds=0)))
        self.end_time.grid(row=0, column=4, padx=5)

        self.vid_player.bind("<<Duration>>", self.pf.update_duration)
        self.vid_player.bind("<<SecondChanged>>", self.pf.update_scale)
        self.vid_player.bind("<<Ended>>", self.pf.video_ended)

        self.skip_plus_5sec = Button(self.control_bar, text=myAttributes.skipp5,
                                     command=lambda: self.pf.skip(self.vid_player, self.progress_slider, self.progress_value, 5))
        self.skip_plus_5sec.grid(row=0, column=5, padx=5)

        self.right_frame.update()

    def preview(self):
        self.preview_window = Frame(
            self.right_frame, width=(self.boss.width/3)*2, height=350)
        self.preview_window.grid(row=0, column=0, padx=0, pady=0)
        # self.preview_window.pack()

        self.vid_player = TkinterVideo(
            scaled=True, master=self.preview_window)
        self.vid_player.pack(expand=True, fill="both")
        self.vid_player.place(relx=0, rely=0, relwidth=1, relheight=1)
        # self.vid_player.grid(row=0, column=0)

    # def load_video(self, vid_player=None, progress_slider=None, play_pause_btn=None, progress_value=None):
    def load_video(self):
        """ loads the video """

        # self.file_path = filedialog.askopenfilename()
        # self.vid_player = vid_player
        print(self.vid_player.video_info())
        if self.vid_player.video_info()["duration"] != 0:
            self.vid_player.stop()
            self.file_path = filedialog.askopenfilename()
            # self.pf.setFilepath(self.file_path)
            myAttributes.filepath = self.file_path
        else:
            self.file_path = filedialog.askopenfilename()
            # self.pf.setFilepath(self.file_path)
            myAttributes.filepath = self.file_path
        # print(ffmpeg.probe(self.file_path))
        if self.file_path:
            self.vid_player.load(self.file_path)
            self.progress_slider.config(to=0, from_=0)
            self.play_pause_btn["text"] = "▶"
            self.pf.play_pause(self.file_path)
            self.progress_value.set(1)
            # print(self.slider1["to"])
            print(int(self.vid_player.video_info()["duration"]))
            print(self.file_path)

    def seek(self, value):
        print(value)
