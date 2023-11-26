from datetime import timedelta
from tkinter import *
from tkinter import Tk, StringVar
from tkinter import ttk
from modules.videoPlayer import videoPlayer
from modules.playerFunc import *
from modules.my_attributes import myAttributes
from modules.imagesToVideo import ImagesToVideo
from tkinter import filedialog
import moviepy.editor as mp
from PIL import Image, ImageTk
import webbrowser





class mainWindow():

    def __init__(self):
        pass

    def start(self):
        self.root: Tk = Tk()
        self.pf = playerFunctions()
        self.root.title("Video Editor")
        # self.root.minsize(800, 500)
        self.width = 1200
        self.height = 630
        self.global_start = 0
        self.global_end = 1


        self.root.minsize(self.width, self.height)
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.maxsize(self.width, self.height)
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        # create a menu item
        self.file_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New ", )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open ", )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Rename ", )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close ", command=lambda :{exit()} )
        self.file_menu.add_separator()
        # create help item
        self.help_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label="help", menu=self.help_menu)
        self.help_menu.add_command(label="Aayush Yadav", command=lambda :self.makeaboutus(0))
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Himanshu Singh", command=lambda :self.makeaboutus(1))
        self.help_menu.add_separator()
        self.help_menu.add_command(label="contact us  ", )
        self.help_menu.add_separator()

        # create notebook
        self.my_notebook = ttk.Notebook(self.root)
        self.my_notebook.pack()
        # self.my_notebook.grid()

        self.statusbar = Frame(self.root , width=self.width)
        # self.statusbar.grid()

        self.status_var = StringVar(value="Ready")
        self.status_label = Label(
            self.statusbar, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor=W , width=20 , height=1)
        self.status_label.pack(side=LEFT, fill=X)
        # status_label.grid(row=1,column=0)

        self.progress_bar = ttk.Progressbar(
            self.statusbar, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.progress_bar.pack(side=LEFT)
        # progress_bar.grid(row=1,column=0)
        # self.progress_bar.start

        # self.statusbar.grid()
        self.statusbar.pack(side=BOTTOM,fill=X , pady=5)

        self.load_cutWindow_1()

        self.load_mergeWindow_2()
        self.load_musicWindow_1()
        self.load_imgtovid_window()

        
        # print(self.cstart_time_s, " ", self.cend_time_s)
        # self.pf.set_sliders(self.cstart_time_s, self.cend_time_s)
        myAttributes.slider1 = self.cstart_time_s
        myAttributes.slider2 = self.cend_time_s

        # self.
        # Create left and right frames

        # left_frame.pack()

        # Create frames and labels in left_frame
        # Label(left_frame,  text="VIDEO",  relief=RAISED).grid(row=0,  column=0,  padx=5,  pady=5)

        self.root.mainloop()

    def load_cutWindow_1(self):
        self.my_frame1 = Frame(
            self.my_notebook, width=self.width, height=self.height, bg="#ffe6e6")
        self.my_frame1.pack(fill="both", expand=1)

        # canvas = Canvas(self.my_frame1, width=500, height=500)
        # canvas.grid(row=1,column=1)
        # canvas.create_image(0, 0, image=self.image, anchor=NW)

        self.my_notebook.add(self.my_frame1, text="CUTS")
        self.right_frame = videoPlayer(self)
        self.left_frame = Frame(
            self.my_frame1,  width=(self.width/3)*1,  height=self.height - 150 , bg="#ffe6e6")
        self.left_frame.grid(row=0,  column=0,  padx=0,  pady=2)

        self.load_btn = Button(self.left_frame, text="Load", width=20, height=5,
                               command=self.right_frame.load_video, bg="lightgreen")
        self.load_btn.grid(row=1,  column=0,  padx=(((self.width/3)*1)/2)-85,
                           pady=5, columnspan=3)

        # self.cut_btn = Button(self.left_frame, text="Cut",
        #                       command=self.pf.video_cut, bg="lightgreen")
        # self.cut_btn.grid(row=2,  column=0,  padx=(((self.width/3)*1)/2)-25,
        #                   pady=5, columnspan=3)

        # self.right_frame = Frame(
        #     self.my_frame1,  width=(self.width/3)*2,  height=500, bg="red", borderwidth="4", relief="groove")
        # self.right_frame.grid(row=0,  column=1,  padx=10,
        #                       pady=5, columnspan=5, rowspan=5)
        # self.right_frame.grid(row=0,  column=1,  padx=3, pady=5)
        # self.right_frame.pack_propagate(False)

        self.bottom_frame = Frame(
            self.my_frame1,  width=self.width, bg="grey", borderwidth=3, relief="groove")
        self.bottom_frame.grid(row=1,  column=0,  padx=0,
                               pady=3, columnspan=2)
        self.bottom_slider()
        # self.load_toolbar()

    def load_mergeWindow_2(self):
        self.my_frame2 = Frame(
            self.my_notebook, width=1200, height=700, bg="#ffe6e6")
        self.my_frame2.pack(fill="both", expand=1)
        self.my_notebook.add(self.my_frame2, text="MERGE")
        self.file_list = []

        self.setup_widgets()

    def load_musicWindow_1(self):
        self.my_frame3 = Frame(self.my_notebook , width= 1200, height=700 , bg="#ffe6e6")
        self.my_frame3.pack(fill=BOTH , expand=1)
        self.my_notebook.add(self.my_frame3 , text="ADD MUSIC")
        self.loadmusictools()

    def load_imgtovid_window(self):
        self.my_frame4 = Frame(self.my_notebook , width= 1200, height=700 ,bg="#ffe6e6" )
        self.my_frame4.pack(fill=BOTH , expand=1)
        self.my_notebook.add(self.my_frame4 , text="Images To Video")
        myscreen = ImagesToVideo(master=self.my_frame4)
        myscreen.mainloop()
        pass

    def loadmusictools(self):
        # Create the widgets
        
        self.mframe = Frame(self.my_frame3 , width=800 , height=400 , bg="#bbe6e9")
        # self.mframe.pack(side=LEFT , padx=50 , pady=50)
        self.mframe.grid(row=2,column=2 , padx=300 , pady= 170)
        self.video_label = Label(self.mframe, text="Video:")
        self.video_entry = Entry(self.mframe , width=40)
        self.video_button = Button(
            self.mframe, text="Browse", width=17,command=self.browse_video, relief="raised",bg="#80dfff")

        self.audio_label = Label(self.mframe, text="Audio:")
        self.audio_entry = Entry(self.mframe, width=40)
        self.audio_button = Button(
            self.mframe, text="Browse",width=17, command=self.browse_audio, relief="raised",bg="#80dfff")

        self.outputNvar = StringVar()
        self.outputName = Label(self.mframe, text="Output Name:")
        self.outputN = Entry(self.mframe,textvariable=self.outputNvar , width=40)

        self.add_button = Button(
            self.mframe, text="Add Audio to Video", command=self.add_audio, relief="raised",bg="lightgreen")

        self.removeAudio = Button(
            self.mframe, text="Remove Audio", command=self.removeaudio, relief="raised",bg="#ff4d88")

        self.toAudio = Button(
            self.mframe, text="Extract Audio", command=self.extractAudio, relief="raised",bg="#b3b3b3")
        
        # Place the widgets on the window
        self.video_label.grid(row=0, column=0 , pady=20 , padx=10)
        self.video_entry.grid(row=0, column=1 , padx=10)
        self.video_button.grid(row=0, column=2 , padx=10)

        self.audio_label.grid(row=1, column=0 , pady=20 , padx=10)
        self.audio_entry.grid(row=1, column=1, padx=10)
        self.audio_button.grid(row=1, column=2 , padx=10)

        self.outputName.grid(row=2, column=0, pady=20, padx=10)
        self.outputN.grid(row=2, column=1, padx=10)

        self.add_button.grid(row=3, column=0 , padx=20 , pady=10)
        self.removeAudio.grid(row=3,column=1,padx=10,pady=10)
        self.toAudio.grid(row=3 , column=2 , padx=20,pady=10)

    def browse_video(self):
        global video_path
        video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        self.video_entry.delete(0, END)
        self.video_entry.insert(0, video_path)


    def browse_audio(self):
        global audio_path
        audio_path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.mp3;*.wav")])
        self.audio_entry.delete(0, END)
        self.audio_entry.insert(0, audio_path)


    def convert_to_mp3(self,audio_path):
        """
        Convert an audio file to mp3 format using ffmpeg.
        Returns the path to the converted file.
        """
        output_path = os.path.splitext(audio_path)[0] + ".mp3"
        command = f'ffmpeg -i "{audio_path}" "{output_path}" -y -hide_banner -loglevel error'
        os.system(command)
        return output_path


    def add_audio(self):
        # Check that both a video and an audio file have been selected
        if not video_path and not audio_path and self.outputNvar == "":
            return

        # Load the video and audio files using moviepy
        video_clip = mp.VideoFileClip(video_path)
        audio_clip = mp.AudioFileClip(self.convert_to_mp3(audio_path))

        # Add the audio to the video
        video_clip = video_clip.set_audio(audio_clip)

        # Generate a filename for the output video
        # output_path = filedialog.asksaveasfilename(
        #     filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        output_path = os.getcwd() + "/" + self.outputNvar.get() + ".mp4"

        # Write the output video file
        video_clip.write_videofile(output_path, codec='libx264')

        # Close the clips
        video_clip.close()
        audio_clip.close()

    def removeaudio(self):
        # Check that both a video and an audio file have been selected
        print(self.outputNvar)

        if not video_path and self.outputNvar == "PY_VAR4":
            return

        # Load the video and audio files using moviepy
        video_clip = mp.VideoFileClip(video_path)
        # audio_clip = mp.AudioFileClip(self.convert_to_mp3(audio_path))

        # Add the audio to the video
        video_clip = video_clip.without_audio()

        # Generate a filename for the output video
        # output_path = filedialog.asksaveasfilename(
        #     filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        output_path = os.getcwd() + "/" + self.outputNvar.get() + ".mp4"
        print(output_path)

        # Write the output video file
        video_clip.write_videofile(output_path , audio=False)

        # Close the clips
        video_clip.close()

    def extractAudio(self):
        # Check that both a video and an audio file have been selected
        if not video_path and not self.outputNvar:
            return

        # Load the video and audio files using moviepy
        video_clip = mp.VideoFileClip(video_path)
        audio_clip = video_clip.audio

        # Add the audio to the video
        # video_clip = video_clip.set_audio(audio_clip)

        # Generate a filename for the output video
        # output_path = filedialog.asksaveasfilename(
        #     filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        output_path = os.getcwd() + "/" + self.outputNvar.get() + ".mp3"

        # Write the output video file
        audio_clip.write_audiofile(output_path)

        # Close the clips
        video_clip.close()
        audio_clip.close()

    def update_listbox(self):
        # clear the Listbox
        self.listbox.delete(0, END)
        # insert items with serial number and divider
        for i, file_name in enumerate(self.file_list, start=1):
            self.listbox.insert(END, f"{i}. {file_name}")
            self.listbox.insert(END, '-' * 50)
        # remove the last divider
        if self.listbox.size() > 0:
            self.listbox.delete(END)

    def add_file(self):
        # open the file dialog and get the selected file name
        file_name = filedialog.askopenfilename()
        if file_name:
            # add the file name to the list
            self.file_list.append(file_name)
            # add the file name to the Listbox
            self.listbox.insert(END, file_name)

    def load_toolbar(self):
        self.tool_bar = Frame(self.left_frame,  width=180,
                              height=185,  bg='grey')
        self.tool_bar.grid(row=2,  column=0,  padx=5,  pady=5, sticky="w")

    def bottom_slider(self):
        self.cut_bottom_frame = Frame(
            self.bottom_frame, width=1200, height=self.height-450, borderwidth=3, relief="groove")
        Label(self.cut_bottom_frame, text="Start time :").grid(row=0, column=0)
        self.cstart_time = IntVar(self.cut_bottom_frame)
        self.cstart_time_s = Scale(self.cut_bottom_frame, variable=self.cstart_time, showvalue=False,
                                   from_=0, to=0, orient="horizontal", length=600, command=self.update_value_0)
        self.cstart_time_s.grid(row=0, column=1, pady=10)
        self.start_label = Label(
            self.cut_bottom_frame, text="00:00:00", width=10)
        self.start_label.grid(row=0, column=2)
        # self.cstart_time_s.config(to=100, from_=0)
        # self.cstart_time_s.pack(side=LEFT)
        Label(self.cut_bottom_frame, text="End time :").grid(row=1, column=0)
        self.cend_time = IntVar(self.cut_bottom_frame)
        self.cend_time_s = Scale(self.cut_bottom_frame, variable=self.cend_time, showvalue=False,
                                 from_=0, to=0, orient="horizontal", length=600, command=self.update_value_1)
        self.cend_time_s.grid(row=1, column=1, pady=10)
        self.end_label = Label(self.cut_bottom_frame,
                               text="00:00:00")
        self.end_label.grid(row=1, column=2, pady=10)
        self.new_file_name = Label(self.cut_bottom_frame,
                                   text="Filename:").grid(row=2, column=0, pady=10)
        self.filename_var = StringVar()
        self.text_box_name = Entry(
            self.cut_bottom_frame, textvariable=self.filename_var, width=99).grid(row=2, column=1)

        self.export_btn = Button(
            self.cut_bottom_frame, text="Export", width=10, bg="#594529", command=lambda: self.pf.video_cut(self.global_start, self.global_end, self.filename_var , self.export_btn , self.status_var , self.progress_bar , self.root)).grid(row=3, columnspan=3, pady=10)
        # self.cend_time_s.pack(side=LEFT)
        self.cut_bottom_frame.grid(row=0, column=0, pady=0, padx=220)
        # self.cut_bottom_frame.pack(side=LEFT, expand=True, fill=BOTH)
        myAttributes.slider1 = self.cstart_time_s
        myAttributes.slider2 = self.cend_time_s
    def bottom_slider_destroy(self):
        self.cut_bottom_frame.destroy()

    def update_value_0(self, value):
        if int(self.global_end) > int(value):
            self.global_start = value
            newvalue = str(timedelta(seconds=int(value)))
            self.start_label["text"] = newvalue
        else:
            self.cstart_time_s.set(self.global_start)

    def update_value_1(self, value):
        if int(self.global_start) < int(value):
            self.global_end = value
            newvalue = str(timedelta(seconds=int(value)))
            self.end_label["text"] = newvalue
        else:
            self.cend_time_s.set(self.global_end)

    def setup_widgets(self):
        self.frame1 = Frame(self.my_frame2)
        self.frame1.pack(side=BOTTOM)

        self.add_file_button = Button(
            self.frame1,bg="#ffe6e6", text='Merge',width=20, command=lambda: self.pf.mergeVideo(self.file_list, self.outputNvar1.get()))
        self.add_file_button.grid(row=1,column=2)
        # self.add_file_button = Button(
        #     self.my_frame2,bg="#ffe6e6", text='Merge',width=20, command=lambda: self.pf.mergeVideo(self.file_list, "tempmerged"))
        # self.add_file_button.pack(side=BOTTOM, padx=10, pady=10)

        self.add_file_button = Button(
            self.frame1, text='Remove File',bg="#ff4d88", width=20,  command=self.remove_file_tree)
        # self.add_file_button.pack(side=BOTTOM, padx=10, pady=10)
        self.add_file_button.grid(row=0,column=1 , columnspan=2 , padx=15)

        self.add_file_button = Button(
            self.frame1, text='Add File', width=20,  command=self.add_file , bg="lightgreen")
        # self.add_file_button.pack(side=BOTTOM, padx=10, pady=10)
        self.add_file_button.grid(row=0,column=0 , columnspan=2, padx=15)

        self.outputNvar1 = StringVar()
        self.outputName1 = Label(self.frame1, text="Output Name:")
        self.outputN1 = Entry(self.frame1,textvariable=self.outputNvar1 , width=40)

        self.outputName1.grid(row=1, column=0, pady=20, padx=10)
        self.outputN1.grid(row=1, column=1, padx=10)

        self.treeview = ttk.Treeview(self.my_frame2, columns=(
            'serial_number', 'file_name', 'duration'))
        self.treeview.heading('serial_number', text='No.')
        self.treeview.heading('file_name', text='File Name')
        self.treeview.heading('duration', text='Duration')

        self.treeview.column('#0', stretch=False, width=0)
        self.treeview.column('serial_number', anchor=CENTER, width=50)
        self.treeview.column('file_name', anchor=CENTER, width=200)
        self.treeview.column('duration', anchor=CENTER, width=50)

        self.treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.treeview.bind("<<TreeviewSelect>>", self.doubleclicked)

    def remove_file_tree(self):
        # self.treeview.delete(self.selected_item)
        # print(self.treeview.selection())
        curitem = self.treeview.item(self.treeview.selection()[0])["values"][0]
        self.treeview.delete(self.treeview.selection()[0])
        self.file_list.pop(curitem-1)
        print(curitem)

    def add_file(self):
        filetypes = [('Video Files', '*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.mpeg *.mpg *.m4v'),
                     ('Image Files', '*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.ico *.webp')]
        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            self.file_list.append(file_path)
            duration = str(timedelta(seconds=int(
                self.get_video_duration(file_path))))
            self.treeview.insert('', END, values=(len(self.file_list), os.path.basename(
                file_path), duration), tags=(len(self.file_list),))

            # update the serial number of the remaining rows
            for i, child in enumerate(self.treeview.get_children(), start=1):
                self.treeview.set(child, 'serial_number', i)
        print(self.file_list)

    def get_video_duration(self, video_path):
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()

        return duration

    def doubleclicked(self, e):
        self.selected_item = self.treeview.selection()[0]

    def makeaboutus(self , c):
        if c == 0:
            url = "https://www.linkedin.com/in/aayush-yadav-ba467820b/"
            webbrowser.open(url)
        else:
            url = "https://www.linkedin.com/in/himanshu-singh-b76964198"
            webbrowser.open(url)
mywindow = mainWindow()
