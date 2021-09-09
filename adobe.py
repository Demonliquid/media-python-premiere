# %% LIBRERIAS
from pymiere import wrappers
from pymiere.wrappers import get_system_sequence_presets
from pymiere.wrappers import time_from_seconds
from pytube import YouTube
import pymiere
import time
import os
import psutil
import subprocess


# %% FUNCIONES
def addVideo(clip,seq,inP,ouP):
    clip.setInPoint(inP, 4)
    clip.setOutPoint(ouP, 4)
    seq.videoTracks[0].insertClip(clip,0)

def cutVideo(clip, seq, inP, ouP, cut):
    clip.setInPoint(inP, 4)
    clip.setOutPoint(cut, 4)
    seq.videoTracks[0].insertClip(clip,0)

    clip.setInPoint(cut, 4)
    clip.setOutPoint(ouP, 4)
    seq.videoTracks[0].insertClip(clip, cut-inP)




def setup():
    process = "Adobe Premiere Pro.exe"
    if not process in (i.name() for i in psutil.process_iter()):
        print("Adobe execution in progress")
        subprocess.Popen([r"C:\Program Files\Adobe\Adobe Premiere Pro 2020\Adobe Premiere Pro.exe"])
        time.sleep(25)
        print("Adobe execution complete")
    else:
        print("Adobe is alredy open")



    # CREAR PROYECTO
    project_path = r'F:\Codigo\On github\media-python-premiere\adobe-test'
    pymiere.objects.app.newProject(project_path)  # Create project



    # CREAR SECUENCIA
    # CONFIG
    sequence_preset_path = get_system_sequence_presets(category="HDV", resolution=None, preset_name="HDV 1080p25")  
    sequence_name = "My new sequence"

    # CREATE
    pymiere.objects.qe.project.newSequence(sequence_name, sequence_preset_path)

    # OPEN
    sequence = [s for s in pymiere.objects.app.project.sequences if s.name == sequence_name][0]
    pymiere.objects.app.project.openSequence(sequenceID=sequence.sequenceID)




# %%
setup()

# %%
































# %% SETUP
# ABRIR ADOBE
process = "Adobe Premiere Pro.exe"
if not process in (i.name() for i in psutil.process_iter()):
    print("Adobe execution in progress")
    subprocess.Popen([r"C:\Program Files\Adobe\Adobe Premiere Pro 2020\Adobe Premiere Pro.exe"])
    time.sleep(25)
    print("Adobe execution complete")
else:
    print("Adobe is alredy open")



# CREAR PROYECTO
project_path = r'F:\Codigo\On github\media-python-premiere\adobe-test'
pymiere.objects.app.newProject(project_path)  # Create project



# %%
# CREAR SECUENCIA
# CONFIG
sequence_preset_path = get_system_sequence_presets(category="HDV", resolution=None, preset_name="HDV 1080p25")  
sequence_name = "My new sequence"

# CREATE
pymiere.objects.qe.project.newSequence(sequence_name, sequence_preset_path)

# OPEN
sequence = [s for s in pymiere.objects.app.project.sequences if s.name == sequence_name][0]
pymiere.objects.app.project.openSequence(sequenceID=sequence.sequenceID)


# %% AGREGAR VIDEO
project = pymiere.objects.app.project
media_path = r'F:\Codigo\On github\media-python-premiere\adobe-test\input\video.mp4'

# import media into Premiere
success = project.importFiles(
    [media_path], # can import a list of media
    suppressUI=True,
    targetBin=project.getInsertionBin(),
    importAsNumberedStills=False
)
# find media we imported
items = project.rootItem.findItemsMatchingMediaPath(media_path, ignoreSubclips=False)
# add clip to active sequence
#project.activeSequence.videoTracks[0].insertClip(items[0], time_from_seconds(0))





# %% Startup
# Check that a project is opened
project_opened, sequence_active = wrappers.check_active_sequence(crash=False)
if not project_opened:
    raise ValueError('please open a project')
project = pymiere.objects.app.project

# Open sequences in UI if none are active
if not sequence_active:
    sequences = wrappers.list_sequences()
    for seq in sequences:
        project.openSequence(sequenceID=seq.sequenceID)
    project.activeSequence = sequences[0]

clips = wrappers.list_video(project.activeSequence)



# %% CORTAR Y AGREGAR
clip = items[0]
cutVideo(clip, project.activeSequence, 100, 200, 150)




# %%





# %% DESCARGAR VIDEO
yt = YouTube(input('Youtube video URL'))
stream = yt.streams.filter(res=input('Resolution as 1080p/720p')).first()
stream.download(input('Location to save video'))
