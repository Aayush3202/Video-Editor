from datetime import timedelta
from tkinter import *
from modules.my_attributes import myAttributes
from moviepy.editor import *
from proglog import *
import time
from threading import Thread


class playerFunctions():
    # file_path = None
    def __init__(self):
        # self.file_path = None
        # self.slider1 = None
        # self.slider2 = None
        pass

    # @set
    # def setVars(self, vid_player):
    #     self.vid_player = vid_player

    def set_sliders(self, slider1, slider2):
        self.slider1 = slider1
        self.slider2 = slider2

    def setVars(self, vid_player, play_pause_btn,
                skip_plus_5sec, start_time, progress_value, progress_slider, end_time):
        self.vid_player = vid_player
        self.play_pause_btn = play_pause_btn
        self.skip_plus_5sec = skip_plus_5sec
        self.start_time = start_time
        self.progress_value = progress_value
        self.progress_slider = progress_slider
        self.end_time = end_time
        # self.file_path = None

    # def setFilepath(self, filepath):
    #     print("set method")
    #     file_path = filepath
    #     print(self.file_path)
    # def load_video(self, vid_player, progress_slider, play_pause_btn, progress_value):
    #     """ loads the video """

    #     self.file_path = filedialog.askopenfilename()
    #     # self.vid_player = vid_player

    #     if self.file_path:
    #         self.vid_player.load(self.file_path)
    #         progress_slider.config(to=0, from_=0)
    #         play_pause_btn["text"] = myAttributes.play
    #         self.play_pause()
    #         progress_value.set(6)
    #         print("hii")

    def seek(self, value=None):
        """ used to seek a specific timeframe """
        # print("hii")
        self.vid_player.seek(int(value))

    def skip(self, vid_player, progress_slider, progress_value, value: int):
        """ skip seconds """
        vid_player.seek(int(progress_slider.get())+value)
        progress_value.set(progress_slider.get() + value)

    def play_pause(self, filepath=None):
        """ pauses and plays """
        if self.vid_player.video_info()["duration"] != 0 or filepath != None:
            if self.vid_player.is_paused():
                self.vid_player.play()
                self.play_pause_btn["text"] = myAttributes.pause
            else:
                self.vid_player.pause()
                self.play_pause_btn["text"] = myAttributes.play

    def video_ended(self, event):
        """ handle video ended """
        self.progress_slider.set(self.progress_slider["to"])
        self.play_pause_btn["text"] = myAttributes.play
        self.progress_slider.set(0)

    def clicked():
        """if button is clicked, display message"""
        print("Clicked.")

    def update_duration(self, event):
        """ updates the duration after finding the duration """
        # pass
        # print(event)
        # time.sleep(0.5)
        duration = self.vid_player.video_info()["duration"]
        # print(self.vid_player.video_info())
        print(duration)
        self.end_time["text"] = str(timedelta(seconds=int(duration)))
        # self.start_time["text"] = str(timedelta(seconds=duration))
        self.progress_slider["to"] = duration
        try:
            myAttributes.slider1["to"] = duration
            myAttributes.slider2["to"] = duration
        except Exception as e:
            print(e)
            pass
        # print(duration)

    def update_scale(self, event):
        """ updates the scale value """
        # pass
        # print("update")
        self.progress_value.set(self.vid_player.current_duration())
        self.start_time["text"] = str(
            timedelta(seconds=int(self.vid_player.current_duration())))

    def video_cut(self, starttime, endtime, filename , boss , status_var,progress_bar , mainb):
        print(myAttributes.filepath, " ", starttime,
              " ", endtime, " ", filename.get())
        print("Hii 1")
        self.progress_bar = progress_bar
        print("Hii 2")
        self.status_var=status_var
        self.progresslog = ProgressBarLogger()
        status_var.set("Proccessing...")
        progress_bar.start()
        mainb.update_idletasks()
        if filename.get() != "" and filename.get() != None:
            try:
                # ffmpeg_extract_subclip("bhoot.mp4", 0,
                #                        4, targetname="test.mp4")
                # loading video gfg
                clip = VideoFileClip(myAttributes.filepath)
                # getting only first 5 seconds
                clip = clip.subclip(starttime, endtime)
                # showing clip
                # clip.ipython_display(width=360)
                filename_f = f"{filename.get()}.mp4"
                # clip.write_videofile(filename_f , verbose = True , threads = 1 , logger = self.progresslog)
                t = Thread(target=self.threadfunc , args=[clip , filename_f , self.progresslog])
                # print(boss)
                print("Hii 7")
                t.start()
                time.sleep(1)
                # self.progress_callback()
                print("Hii 8")
                # t.join()
            except Exception as e:
                print(e)
        # status_var.set("Completed")
        # progress_bar.stop()
    
    def mergeVideo(self , videos_lst , filename):
        newlst = []
        print(videos_lst)
        print(len(videos_lst))
        if len(videos_lst) > 0:
            for i in range(len(videos_lst)):
                print(i)
                print(videos_lst[i])
                newlst.append(VideoFileClip(videos_lst[i]))
            
            merged_video = concatenate_videoclips(newlst , method="compose")
            merged_video.write_videofile(f"{filename}.mp4" , threads=10)
        
    def progress_callback(self):
        # print(args)
        # status_var.set("Wait")
        while True:
            try:
                # time.sleep(1)
                # mylog = self.progresslog.logs
                mylog = self.progresslog.state
                # print(mylog)
                # {'bars': OrderedDict([('chunk', {'title': 'chunk', 'index': 287, 'total': 287, 'message': None, 'indent': 0}), ('t', {'title': 't', 'index': 75, 'total': 312, 'message': None, 'indent': 2})]), 
                # 'message': 'Moviepy - Writing video asdsda.mp4\n'}
                # temp = dict(mylog["bars"])
                # print(temp["chunk"]["index"])
                # print(mylog["bars"]["chunk"]["index"])
                # continue
                totalindex = mylog["bars"]["t"]["total"]
                # print(totalindex)
                currentindex = mylog["bars"]["t"]["index"]
                # print(currentindex)
                # print(mylog)
                print(f"{currentindex}/{totalindex}" , end="\r")
                # self.update_progress(totalindex , currentindex , progress_bar , status_var)
                percent = int((currentindex / totalindex) * 100)
                self.progress_bar['value'] = percent
                self.status_var.set(f"Progress: {percent}%")
                
                # time.sleep(1)
                if totalindex == currentindex:
                    break
                # print(self.progresslog.logs)
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                print(e)
                continue

    def threadfunc(self , myclip , filename_f , progress):
        try:
            # print(self.status_var.get())
            myclip.write_videofile(filename_f , verbose = True , threads = 5, logger = progress)
            self.completed()
        except Exception as e:
            print(e)
            pass

        # print("Processing progress: {:.2f}%".format(percentage * 100))
    # def mediaDetails():
    def completed(self):
        self.status_var.set("Completed")
        self.progress_bar.stop()
    def update_progress(self,total, current, progress_bar, status_var):
        percent = int((current / total) * 100)
        # print(progress_bar['value'])
        print(status_var.get())
        progress_bar['value'] = percent
        status_var.set(f"Progress: {percent}%")
