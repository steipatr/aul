import os
import sys

import pyNetLogo
import imageio

netlogo = pyNetLogo.NetLogoLink(gui=False)


def export_png(model, tick, params=None, png='pynevex.png',setup='Setup',go='go'):
    """Export a single tick from a NetLogo run as a PNG
    
    Parameters
    ----------
    model: str
        Path, name of NetLogo model file
        
    tick: int
        Model time step to export
        
    params: dict
        Pairings of NetLogo global parameters (e.g. sliders) and desired values
        
    png: str
        Name of created PNG
        
    setup: str
        Name of model's initialization procedure
        
    go: str
        Name of model's iteration procedure
    
    Returns
    -------
    None (PNG file created in model directory)
    
    """
    
    frame = [tick]
    
    export_frames(model, frame, params, setup, go)
    
    rename_frame(frame, png)
    
    return

def export_gif(model, ticks, params=None, gif=None, setup='Setup', go='go', fps=10, subrectangles=False):
    """Export multiple ticks from a NetLogo run as a GIF
    
    Parameters
    ----------
    model: str
        Path, name of NetLogo model file
        
    ticks: int, range of ints, list of ints
        Model time steps to export
        
    params: dict
        Pairings of NetLogo global parameters (e.g. sliders) and desired values
        
    gif: str
        Name of created GIF
        
    setup: str
        Name of model's initialization procedure
        
    go: str
        Name of model's iteration procedure
        
    fps: int
        GIF speed in frames per second
        
    subrectangles: Boolean
        Use subrectangles to compress GIF
    
    Returns
    -------
    None (GIF file created in model directory)
    
    """
        
    frame_list = build_frame_list(ticks)
    
    export_frames(model, frame_list, params, setup, go)
    
    file_name = make_name(model, gif, ending='.gif')
    
    build_gif(frame_list, file_name, fps, subrectangles)
    
    delete_frames(frame_list)
    
    return

def export_mp4(model, ticks, params=None, mp4=None, setup='Setup', go='go', fps=10, quality=5):
    """Export multiple ticks from a NetLogo run as an MP4
    
    Parameters
    ----------
    model: str
        Path, name of NetLogo model file
        
    ticks: int, range of ints, list of ints
        Model time steps to export
        
    params: dict
        Pairings of NetLogo global parameters (e.g. sliders) and desired values
        
    mp4: str
        Name of created MP4
        
    setup: str
        Name of model's initialization procedure
        
    go: str
        Name of model's iteration procedure
        
    fps: int
        MP4 speed in frames per second
        
    quality: int, [1-10]
        color accuracy and sharpness of MP4, 10 is best quality
    
    Returns
    -------
    None (MP4 file created in model directory)
    
    """
    
    frame_list = build_frame_list(ticks)
    
    export_frames(model,frame_list, params, setup, go)
    
    file_name = make_name(model, mp4, ending='.mp4')
    
    build_mp4(frame_list, file_name, fps, quality)
    
    delete_frames(frame_list)
    
    return

def build_frame_list(ticks):
    """convert desired ticks supplied as range into list"""
    
    #range of ticks. [0,5] -> 0,1,2,3,4
    if len(ticks) == 2:
        save_frames = list(range(ticks[0],ticks[1],1))

    #range of ticks with spacing. [0,50,10] -> 0,10,20,30,40
    elif len(ticks) == 3:
        save_frames = list(range(ticks[0],ticks[1],ticks[2]))

    #explicit list of ticks
    else:
        save_frames = ticks
    
    return save_frames

def export_frames(model,save_frames,params,setup,go):
    """load NetLogo model, initialize, run up to each desired tick, export current world view as PNG, continue to next tick, etc. 
    PNGs saved in directory of model.
    """
    
    netlogo.load_model(str(model))
    
    #overwrite model parameter settings if supplied
    if params != None:
        #modified from pyNetLogo docs, credit Jan Kwakkel and Marc Jaxa-Rozen
        for k,v in params.items():
            if k == "random-seed":
                #The NetLogo random seed requires a different syntax
                netlogo.command('random-seed {}'.format(v))
            else:
                #Otherwise, assume the input parameters are global variables
                netlogo.command('set {0} {1}'.format(k,v))            
              
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
                previous_frame = save_frames[save_frames.index(frame)-1]
                interval = frame - previous_frame
            
            netlogo.command('repeat ' + str(frame) +  '[' + go + ']')

            netlogo.command('export-view \"' + str(frame) + '.png\" ')
        
    return

def make_name(model, passed_name=None,ending=None):
    """Determine name of file to be created."""
    
    if passed_name == None:
        file_name = model.split('.')[0] + ending
        
    else: 
        if len(passed_name.split('.')) > 1:
            file_name = passed_name
        else:
            file_name = passed_name + ending
    
    return file_name

def build_gif(save_frames,gif,fps,subrectangles):
    """Join exported PNG world views into GIF using desired settings."""
    
    images = []
    for frame in save_frames:
        images.append(imageio.imread(str(frame) + '.png'))
    imageio.mimsave(gif, images, fps=fps, subrectangles=subrectangles)      
    return

def build_mp4(save_frames,mp4,fps,quality):
    """Join exported PNG world views into MP4 using desired settings."""
    
    images = []
    for frame in save_frames:
        images.append(imageio.imread(str(frame) + '.png'))
    imageio.mimsave(mp4, images, fps=fps, quality=quality)      
    return

def delete_frames(save_frames):
    """Remove exported PNG world views to avoid clutter."""
    
    cwd = os.getcwd()
    for frame in save_frames:
        frame_name = str(frame) + '.png'
        frame_path = os.path.join(cwd, frame_name)
        if os.path.isfile(frame_path):
            os.unlink(frame_path)
    return

def rename_frame(frame, png):
    """Ensure consistent naming of exported PNG world views."""
    
    os.rename(str(frame[0]) + '.png', png)
    return