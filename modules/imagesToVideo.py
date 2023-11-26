import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
import ffmpeg
import moviepy.editor as mp
from pydub import AudioSegment

class ImageBox(tk.Canvas):
    def __init__(self, master, images, *args, **kwargs):
        super().__init__(master, width=800, height=300, *args, **kwargs)
        self.images = images
        self.photo_images = []
        self.dragging = None
        self.frame = tk.Frame(self, bg='#ffe6e6')
        self.vscrollbar = tk.Scrollbar(self, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=self.vscrollbar.set)
        self.create_window((0, 0), window=self.frame, anchor='nw')
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.frame.bind('<Configure>', self.on_frame_configure)
        self.draw_images()

    def draw_images(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        row, col = 0, 0
        for image_path in self.images:
            img = Image.open(image_path)
            img.thumbnail((180, 180))
            photo_image = ImageTk.PhotoImage(img)
            self.photo_images.append(photo_image)
            image_frame = tk.Frame(self.frame, width=200, height=200, padx=10, pady=10, bg="#bbe6e9")
            image_frame.grid(row=row, column=col, padx=5, pady=5)
            image_label = tk.Label(image_frame, image=photo_image, bg='white')
            image_label.pack(fill='both', expand=True)
            text_label = tk.Label(image_frame, text=os.path.basename(image_path), bg='white')
            text_label.pack()
            col += 1
            if col == 4:
                col = 0
                row += 1

    def on_click(self, event):
        self.dragging = self.frame.winfo_containing(event.x_root, event.y_root)

    def on_drag(self, event):
        if self.dragging:
            self.frame.move(self.dragging, event.x - self.dragging.winfo_rootx(), event.y - self.dragging.winfo_rooty())

    def on_release(self, event):
        if self.dragging:
            x, y = self.dragging.winfo_x(), self.dragging.winfo_y()
            col = x // 210
            row = y // 210
            index = row * 3 + col
            self.images.remove(self.dragging.image_path)
            self.images.insert(index, self.dragging.image_path)
            self.draw_images()
            self.dragging = None

    def on_frame_configure(self, event):
        self.configure(scrollregion=self.bbox('all'))

class ImagesToVideo(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.images = []
        self.image_box = ImageBox(self, self.images, bg='white')
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.image_box.yview)
        self.image_box.configure(yscrollcommand=self.scrollbar.set)
        self.browse_button = tk.Button(self, text='Browse', command=self.browse_folder,bg="#80dfff")

        self.putthisframe = tk.Frame(self)
        self.putthisframe.grid(row=2 , column=0)

        self.addaudioL = tk.Label(self.putthisframe , text="Add Audio")
        self.audio_input_box = tk.Entry(self.putthisframe)
        self.audio_browse_button = tk.Button(self.putthisframe, text='Browse Audio', command=self.browse_audio_file,bg="#80dfff")
        self.convert_button = tk.Button(self.putthisframe, text='Convert to Video', command=self.convert_to_video,bg="lightgreen")

        self.outputfilename = tk.Label(self.putthisframe , text="Output filename")
        self.output_input_box = tk.Entry(self.putthisframe)

        self.pack()
        self.image_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.browse_button.grid(row=1, column=0, padx=10, pady=10)
        self.addaudioL.grid(row=0,column=0,padx=10,pady=10)
        self.audio_input_box.grid(row=0, column=1, padx=10, pady=10)
        self.audio_browse_button.grid(row=0, column=2, padx=10, pady=10)
        self.outputfilename.grid(row=1,column=0 , padx=10 , pady=10)
        self.output_input_box.grid(row=1,column=1,padx=10 , pady=10)

        self.convert_button.grid(row=2, column=1, padx=10, pady=10)
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
            print(self.images)
            self.image_box.images = self.images
            self.image_box.draw_images()

    def browse_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Audio Files', '*.wav *.mp3')])
        if file_path:
            self.audio_file = file_path
            self.audio_input_box.delete(0, tk.END)
            self.audio_input_box.insert(0, file_path)

    def convert_to_video(self):
        if not self.images:
            tk.messagebox.showerror('Error', 'Please select images')
        else:
            outputname = self.output_input_box.get() + ".mp4"
            if self.audio_input_box.get():
                self.images_to_video(self.images , outputname , 0.5 , self.audio_input_box.get())
            else:
                self.images_to_video(self.images , outputname , 0.5)
    

    def images_to_video(self,images_path, output_path, fps, audio_path=None):
        # get image dimensions
        # print(images_path[0])
        img = cv2.imread(images_path[0])
        # img = cv2.imread(os.path.join(images_path, os.listdir(images_path)[0]))
        height, width, channels = img.shape

        # create video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # choose video codec
        # fourcc = cv2.VideoWriter_fourcc(*'libx264')  # choose video codec
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # loop through images and add them to video
        for image_file in images_path:
            # image_path = os.path.join(images_path, image_file)
            print(image_file)
            img = cv2.imread(image_file)
            img = cv2.resize(img , (width,height))
            # cv2.imshow("abc" , img)
            # cv2.waitKey(0)
            video_writer.write(img)

        # release video writer object
        video_writer.release()

        # add audio to video if audio_path is provided
        if audio_path:
            self.add_audio(output_path , audio_path)
            # pass
            # audio = cv2.VideoCapture(audio_path)
            # video = cv2.VideoCapture(output_path)

            # # get audio and video properties
            # audio_fps = audio.get(cv2.CAP_PROP_FPS)
            # audio_frame_count = int(audio.get(cv2.CAP_PROP_FRAME_COUNT))
            # video_fps = video.get(cv2.CAP_PROP_FPS)
            # video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            # # set audio and video frame position to start at the beginning
            # audio.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # video.set(cv2.CAP_PROP_POS_FRAMES, 0)

            # # create new video writer object with audio
            # temp_path = os.path.join(images_path, 'temp.mp4')
            # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            # temp_video_writer = cv2.VideoWriter(temp_path, fourcc, video_fps, (width, height), isColor=True)

            # # loop through video frames and add audio
            # for i in range(video_frame_count):
            #     ret, video_frame = video.read()
            #     ret, audio_frame = audio.read()

            #     # stop loop if end of audio is reached
            #     if not ret:
            #         break

            #     # add audio to video frame
            #     temp_video_writer.write(video_frame)
            #     temp_video_writer.write(video_frame)

            # # release video and audio objects
            # temp_video_writer.release()
            # video.release()
            # audio.release()

            # replace original video with video with audio
            # os.remove(output_path)
            # os.rename(temp_path, output_path)

    def add_audio(self , video_path , audio_path):
        # Check that both a video and an audio file have been selected
        if not video_path and not audio_path and audio_path == "":
            return

        
        # Load the video and audio files using moviepy'
        print("Hii 1")
        video_clip = mp.VideoFileClip(video_path)
        print("Hii 1")
        # audio_clip = mp.AudioFileClip(self.convert_to_mp3(audio_path))
        audio_clip = mp.AudioFileClip(audio_path)
        print("Hii 1")


        print(video_clip.duration)
        # audio_clip = audio_clip.set_duration(video_clip.duration)
        audio_clip = audio_clip.subclip(0 , int(video_clip.duration))

        # Combine audio clip with video clip
        # final_clip = video_clip.set_audio(mp.CompositeAudioClip([audio_clip]))
        final_clip = video_clip.set_audio(audio_clip)

        # Write the final clip to disk
        # final_clip.write_videofile(output_path, audio_codec='aac', threads=4)
        # Add the audio to the video
        # video_clip = video_clip.set_audio(audio_clip)

        # Generate a filename for the output video
        # output_path = filedialog.asksaveasfilename(
        #     filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        output_path = os.getcwd() + "/" + "temp.mp4"
        # new_output_path = os.getcwd() + "/" + "temp1.mp4"

        # Write the output video file
        # video_clip.write_videofile(output_path, codec='libx264')
        # final_clip.write_videofile(output_path, codec='libx264' , audio_codec="aac", threads=4)
        final_clip.write_videofile(output_path, codec='libx264')
        # (
        #     ffmpeg
        #     .input(output_path)
        #     .output(new_output_path, vcodec='libx264', preset='slow', crf=22, acodec='aac', audio_bitrate='128k', audio_channels=2)
        #     .run()
        # )
        # ffmpeg_cmd = f"ffmpeg -i {output_path} -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k -ac 2 {output_path}"
        # os.system(ffmpeg_cmd)

        # Close the clips
        video_clip.close()
        audio_clip.close()

        os.remove(video_path)
        # os.remove(output_path)
        # os.rename(new_output_path , video_path)
        os.rename(output_path , video_path)
    def convert_to_mp3(self,audio_path):

        # output_path = os.path.splitext(audio_path)[0] + ".mp3"
        output_path = os.getcwd() + "/temp.mp3"
        print(output_path)
        # (
        #     ffmpeg
        #     .input(audio_path)
        #     .output(output_path, acodec='libmp3lame', ar=44100, ab='128k')
        #     .run()
        # )
        audio = AudioSegment.from_file(audio_path)

        # Export audio file as MP3 format
        audio.export(output_path, format='mp3', bitrate='128k')
        # command = f'ffmpeg -i "{audio_path}" "{output_path}" -y -hide_banner -loglevel error'
        # os.system(command)
        return output_path

# if __name__ == '__main__':
#     root = tk.Tk()
#     app = Application(master=root)
#     app.mainloop()
