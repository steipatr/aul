import os
import sys

import pyNetLogo
import imageio

from PIL import Image, ImageEnhance

netlogo = pyNetLogo.NetLogoLink(gui=False)


def export_png(model, tick, params=None, scale=1.0, png='pynevex.png',setup='Setup',go='go'):
    """Export a single tick from a NetLogo run as a PNG
    
    Parameters
    ----------
    model: str
        Path, name of NetLogo model file
        
    tick: int
        Model time step to export
        
    params: dict
        Pairings of NetLogo global parameters (e.g. sliders) and desired values
        
    scale: float
        Scale factor by which output file should be larger (or smaller) than NetLogo model world:
            >1.0 larger
            1.0 same size
            <1.0 smaller
        
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

def export_gif(model, ticks, params=None, scale=1.0, fade=0.0, name=None, setup='Setup', go='go', fps=10, subrectangles=False):
    """Export multiple ticks from a NetLogo run as a GIF
    
    Parameters
    ----------
    model: str
        Path, name of NetLogo model file
        
    ticks: int, range of ints, list of ints
        Model time steps to export
        
    params: dict
        Pairings of NetLogo global parameters (e.g. sliders) and desired values
                
    scale: float
        Scale factor by which output file should be larger (or smaller) than NetLogo model world:
            >1.0 larger
            1.0 same size
            <1.0 smaller
                        
    fade: float
        Fade out end of model run to show terminating. Parameter sets duration of fade: 
            0 no fade
            1 start fading immediately
        
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
        
    frames = find_frames(ticks)
    
    export_frames(model, frames, params, setup, go)
    
    file_name = make_name(model, name, ending='.gif')
    
    if scale != 1.0:
        resize_frames(frames, scale)
        
    if fade != 0.0:
        fade_end(frames,fade)
    
    build_gif(frames, file_name, fps, subrectangles)
    
    delete_frames(frames)
    
    return

def export_mp4(model, ticks, params=None, scale=1.0, fade=0.0, name=None, setup='Setup', go='go', fps=10, quality=10):
    """Export multiple ticks from a NetLogo run as an MP4
    
    Parameters
    ----------
    model: str
        Path, name of NetLogo model file
        
    ticks: int, range of ints, list of ints
        Model time steps to export
        
    params: dict
        Pairings of NetLogo global parameters (e.g. sliders) and desired values
                
    scale: float
        Scale factor by which output file should be larger (or smaller) than NetLogo model world:
            >1.0 larger
            1.0 same size
            <1.0 smaller
                        
    fade: float
        Fade out end of model run to show terminating. Parameter sets duration of fade: 
            0 no fade
            1 start fading immediately
        
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
    
    frames = find_frames(ticks)
    
    export_frames(model, frames, params, setup, go)
    
    file_name = make_name(model, name, ending='.mp4')
    
    if scale != 1.0:
        resize_frames(frames, scale)
    
    if fade != 0.0:
        fade_end(frames,fade)
    
    build_mp4(frames, file_name, fps, quality)
    
    delete_frames(frames)
    
    return

def find_frames(ticks):
    """build list of desired export ticks"""
    
    if type(ticks) == int:
        frames = list(range(0,ticks,1))
    
    elif type(ticks) == list:
        
        #range of ticks. [0,5] -> 0,1,2,3,4
        if len(ticks) == 2:
            frames = list(range(ticks[0],ticks[1],1))

        #range of ticks with spacing. [0,50,10] -> 0,10,20,30,40
        elif len(ticks) == 3:
            frames = list(range(ticks[0],ticks[1],ticks[2]))

        #explicit list of ticks
        else:
            frames = ticks
    
    return frames

def export_frames(model,frames,params,setup,go):
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
    
    if len(frames) == 1:
        frame = frames[0]
        netlogo.command('repeat ' + str(frame) +  '[' + go + ']')
        netlogo.command('export-view \"' + str(frame) + '.png\" ')
                
    else:
        for frame in frames:        
            #run for number of ticks between two frames of interest
            if frames.index(frame) == 0: 
                interval = frame
            else:
                previous_frame = frames[frames.index(frame)-1]
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

def build_gif(frames,gif,fps,subrectangles):
    """Join exported PNG world views into GIF using desired settings."""
    
    images = []
    for frame in frames:
        images.append(imageio.imread(str(frame) + '.png'))
    imageio.mimsave(gif, images, fps=fps, subrectangles=subrectangles)      
    return

def build_mp4(frames,mp4,fps,quality):
    """Join exported PNG world views into MP4 using desired settings."""
    
    images = []
    for frame in frames:
        images.append(imageio.imread(str(frame) + '.png'))
    imageio.mimsave(mp4, images, fps=fps, quality=quality, pixelformat='yuvj444p') 
    return

def delete_frames(frames):
    """Remove exported PNG world views to avoid clutter."""
    
    cwd = os.getcwd()
    for frame in frames:
        frame_name = str(frame) + '.png'
        frame_path = os.path.join(cwd, frame_name)
        if os.path.isfile(frame_path):
            os.unlink(frame_path)
    return

def rename_frame(frame, png):
    """Ensure consistent naming of exported PNG world views."""
    
    os.rename(str(frame[0]) + '.png', png)
    return

def resize_frames(frames,scale):
    """Resize all frames."""
    
    for frame in frames:
        infile = Image.open(str(frame) + ".png")
        outsize = (int(infile.size[0]*scale), int(infile.size[1]*scale)) 
        outfile = infile.resize(outsize)
        outfile.save(str(frame) + ".png",format="PNG")  
    return

def fade_end(frames,fade):
    """Fade last few frames of a model run to black."""
    
    #determine which frames to fade
    first_fade = int(len(frames) * (1 - fade))
    fade_frames = frames[first_fade:]
    
    fade_val = 1  
    for frame in fade_frames:
        fade_val = fade_val - (1 / len(fade_frames))
        
        infile = Image.open(str(frame) + ".png")
        outfile = ImageEnhance.Brightness(infile).enhance(fade_val)
        outfile.save(str(frame) + ".png",format="PNG")
    return