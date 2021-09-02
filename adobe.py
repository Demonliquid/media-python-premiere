# %% LIBRERIAS
import pymiere
from pymiere import wrappers
import time
import os
import psutil
import subprocess



# %% EJECUCION

# %% ABRIR ADOBE
process = "Adobe Premiere Pro.exe"
if not process in (i.name() for i in psutil.process_iter()):
    print("Adobe execution in progress")
    subprocess.Popen([r'F:/Adobe Premiere/Adobe Premiere Pro 2020/Adobe Premiere Pro.exe'])
    print("Adobe execution complete")
else:
    print("Adobe is alredy open")

# %% TEST
print(pymiere.objects.app.isDocumentOpen())



# %% CREATE PROJECT
project_path = r"F:\Codigo\On github\media-python-premiere\adobe-test\test.prproj"
# create new empty project
pymiere.objects.app.newProject(project_path)  # from Premiere 2020


# %%
# open existing project
pymiere.objects.app.openDocument(project_path)




# %%
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







cutVideo(clip, project.activeSequence, 10, 20, 15)


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


# list all videos clip in the active sequence
clips = wrappers.list_video(project.activeSequence)
clips[0].components

# get sequence fps (timebase in ticks to be converted to frame per seconds)
fps = 1/(float(project.activeSequence.timebase)/wrappers.TICKS_PER_SECONDS)
print(f"sequence as a framerate of {fps} fps")

# select the first clip in the timeline
clips[0].setSelected(True, True)

# %%







# %% START ADOBE
os.system(r'start F:\Adobe Premiere\Adobe Premiere Pro 2020\Adobe Premiere Pro.exe') 





# %%

# %%

# %%
