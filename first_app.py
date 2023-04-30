from tkinter import *
import pygame 
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root =Tk()
root.title('Codemy.com MP3 Player')
root.iconbitmap('C:/Users/GIAP/OneDrive/Pictures/Ico/icons8-shutdown-64.ico')
root.geometry("500x400")

# Initialze Pygame Mixer
pygame.mixer.init()

# Grab Song Length Time Info
def play_time():
    # Check for double timing
    if stopped:
        return
    # Garb Current Song Elapsed Time
    current_time = pygame.mixer.music.get_pos() / 1000

    # Throw up temp label to get data
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')

    # Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Get Currently Playing Song
    # current_song = song_box.curselection()
    # Grab song title from playlist
    song = song_box.get(ACTIVE)
    # Add directory structure and mp3 to song title
    song = f'D:/Python/musics/{song}.mp3'
    # Load Song with Mutagen
    song_mut = MP3(song)
    # Get song Length 
    global song_length
    song_length = song_mut.info.length
    # Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase current time by 1 second
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} of {converted_song_length}')

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        # Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # Convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')

        # Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # Output time to status bar
    # status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
    
    # Update slider position value to current song position ...
    # my_slider.config(value=int(current_time))

    # fake_label = Label(root, text=int(current_time))
    # fake_label.pack(pady=10)


    # Update time
    status_bar.after(1000, play_time)


# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetype=(("mp3 Files", "*.mp3"), ))
    
    # strip out the directory  info and .mp3 extension from the song name
    song = song.replace("D:/Python/musics/", "")
    song = song.replace(".mp3", "")

    # Add song to listbox
    song_box.insert(END, song)

# Add Many Song To Playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetype=(("mp3 Files", "*.mp3"), ))

    # Loop thru song list and replace directory info and mp3
    for song in songs:
        song = song.replace("D:/Python/musics/", "")
        song = song.replace(".mp3", "")
        # Insert into playlist
        song_box.insert(END, song)

# Play selected song
def play():
    # Set Stopped Variable To False So Song Can Play
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'D:/Python/musics/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call the play_time function to get song length
    play_time()

    # Update Slider To position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)



# Stop playing current song 
global stopped
stopped = False

def stop():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stop Song From Playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear The Status Bar
    status_bar.config(text='')

    # Set Stop Variable To True
    global stopped
    stopped = True

# Play The Next Song in the playlist
def next_song():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # Add directory structure and mp3 to song title
    song = f'D:/Python/musics/{song}.mp3'
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Set Active Bar to next song
    song_box.selection_set(next_one, last=None)

# Play Previous Song In Playlist
def previous_song():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]-1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # Add directory structure and mp3 to song title
    song = f'D:/Python/musics/{song}.mp3'
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Set Active Bar to next song
    song_box.selection_set(next_one, last=None)

# Delete A Song
def delete_song():
    stop()
    # Delete Currently Selected Song
    song_box.delete(ANCHOR)
    # Stop music if it is playing
    pygame.mixer.music.stop()

# Delete All Songs From Playlist
def delete_all_songs():
    # Delete All Songs
    song_box.delete(0, END)
    # Stop music if it is playing
    pygame.mixer.music.stop()


# Create Clobal Pause Variable
global paused
paused = False

# Pause and Unpause The Current Song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Create slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'D:/Python/musics/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))



# Create Playlist Box
song_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# Define Player Control Buttons Images
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/next_button.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop_button.png')

# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()

# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10) 
forward_button.grid(row=0, column=1, padx=10) 
play_button.grid(row=0, column=2, padx=10) 
pause_button.grid(row=0, column=3, padx=10) 
stop_button.grid(row=0, column=4, padx=10) 

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Add Many Song To Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)


# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Create Music Position Slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.pack(pady=30)

# Create Temporary Slider Label
# slider_label = Label(root, text="0")
# slider_label.pack(pady=10)

root.mainloop()
