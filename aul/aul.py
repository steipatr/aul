import os
import sys

import pyNetLogo
import imageio

netlogo = pyNetLogo.NetLogoLink(gui=False)


def export_png(model, tick, png='pynevex.png',setup='Setup',go='go'):
    frame = [tick]
    
    export_frames(model, frame, setup, go)
    
    rename_frame(frame, png)
    
    return

def export_gif(model, ticks, gif=None, setup='Setup', go='go', fps=10, subrectangles=False):
    frame_list = build_frame_list(ticks)
    
    export_frames(model, frame_list, setup, go)
    
    file_name = make_name(model, gif, ending='.gif')
    
    build_gif(frame_list, file_name, fps, subrectangles)
    
    delete_frames(frame_list)
    
    return

def export_mp4(model, ticks, mp4=None, setup='Setup', go='go', fps=10, quality=5):
    frame_list = build_frame_list(ticks)
    
    export_frames(model,frame_list, setup, go)
    
    file_name = make_name(model, mp4, ending='.mp4')
    
    build_mp4(frame_list, file_name, fps, quality)
    
    delete_frames(frame_list)
    
    return

def build_frame_list(ticks):
    if len(ticks) == 2:
        save_frames = list(range(ticks[0],ticks[1],1))

    elif len(ticks) == 3:
        save_frames = list(range(ticks[0],ticks[1],ticks[2]))

    else:
        save_frames = ticks
    
    return save_frames

def export_frames(model,save_frames,setup,go):
    netlogo.load_model(str(model))
    netlogo.command(setup)
    
    if len(save_frames) == 1:
        frame = save_frames[0]
        netlogo.command('repeat ' + str(frame) +  '[' + go + ']')
        netlogo.command('export-view \"' + str(frame) + '.png\" ')
                
    else:
        for frame in save_frames:        
            #run for number of ticks between two frames of interest
            if save_frames.index(frame) == 0: 
                interval = frame
            else:
                previous_frame = save_frames[save_frames.index(frame)-1] #TODO indexing seems ugly
                interval = frame - previous_frame
            
            netlogo.command('repeat ' + str(frame) +  '[' + go + ']')

            netlogo.command('export-view \"' + str(frame) + '.png\" ')
        
    return

def make_name(model, passed_name=None,ending=None):
    if passed_name == None:
        file_name = model.split('.')[0] + ending
        
    else: 
        if len(passed_name.split('.')) > 1:
            file_name = passed_name
        else:
            file_name = passed_name + ending
    
    return file_name

def build_gif(save_frames,gif,fps,subrectangles):
    images = []
    for frame in save_frames:
        images.append(imageio.imread(str(frame) + '.png'))
    imageio.mimsave(gif, images, fps=fps, subrectangles=subrectangles)      
    return

def build_mp4(save_frames,mp4,fps,quality):
    images = []
    for frame in save_frames:
        images.append(imageio.imread(str(frame) + '.png'))
    imageio.mimsave(mp4, images, fps=fps, quality=quality)      
    return

def delete_frames(save_frames):
    cwd = os.getcwd()
    for frame in save_frames:
        frame_name = str(frame) + '.png'
        frame_path = os.path.join(cwd, frame_name)
        if os.path.isfile(frame_path):
            os.unlink(frame_path)
    return

def rename_frame(frame, png):
    os.rename(str(frame[0]) + '.png', png)
    return