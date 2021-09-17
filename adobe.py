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
import urllib.request


# %%
'''
Configuracion previa:
- Premiere version:
- Premiere tiene que tener activada opcion: > Edit > Preferences
                                            > Media > Default Media Scaling
                                            > Scale to frame size
- Tener creado proyecto con secuencias.


STEPS:
1 - Download video
2 - Open Adobe and Template proyect
3 - Import video folder
4 - Cut video and select background
5 - Background: None (black), White, Blur



TODO:
- CAMBIAR LISTA DE VIDEOS POR NOMBRE
- PONER LINK DE DESCARGA Y QUE PIDA DIRECTAMENTE LOS TIEMPOS DE CORTE (SIEMPRE 480p)
- AGREGAR EFECTO CROP: CROP TOP, BOTTOM, LEFT, RIGHT
- NO SOLO BACKGROUND.PNG SINO QUE CUALQUIER OTRA IMAGEN
- ESCALA VIDEO PRINCIPAL 185 - NO EN 16:9 - REVISAR
- Adobe Media Enconder: PRESET > QUEUE > START QUEUE
- EXPORTAR CADA VIDEO DE LA SECUENCIA COMO VIDEO1-VIDEO2-VIDEO3 (con nombres v1/v2/v3/etc... cada uno)
- UI
'''



# %% FUNCIONES
def descargarvideo(youtubeurl, savepath):
    '''It downloads a video from youtube in 480p and solid background'''
    yt = YouTube(youtubeurl)
    stream = yt.streams.filter(res='480p').first()
    stream.download(savepath)
    try:
        whitebackgroundurl = "https://i.imgur.com/AizUHEf.png"
        urllib.request.urlretrieve(whitebackgroundurl, f"{savepath}/white-background.png")
    except:
        pass


def setup(adobe_exe):
    '''Opens Adobe'''
    # ABRIR ADOBE
    process = "Adobe Premiere Pro.exe"
    if not process in (i.name() for i in psutil.process_iter()):
        print("Adobe execution in progress")
        subprocess.Popen([adobe_exe])
        print("Adobe execution complete")
    else:
        print("Adobe is alredy open")


def abrirproyecto(template_file):
    '''Open template project, it tries a couple of times because of Adobe slow execution'''
    attempts = 0
    while attempts < 10:
        time.sleep(1)
        try:
            pymiere.objects.app.openDocument(template_file)
            break
        except:
            attempts +=1


def importvideo(media_path):
    '''Imports folder from descargarvideo() '''
    project = pymiere.objects.app.project
    media_path = media_path

    # import media into Premiere
    success = project.importFiles(
        [media_path], # can import a list of media
        suppressUI=True,
        targetBin=project.getInsertionBin(),
        importAsNumberedStills=False
    )
    # find media we imported
    items = project.rootItem.findItemsMatchingMediaPath(media_path, ignoreSubclips=False)
    return project, items


def listarvideos(items):
    '''Adobe uses an index to use videos, at least for now'''
    for i in range(len(items)):
        print(f"Nombre del video {i}:", items[i].name)


def addVideo(clip,seq,inP,ouP, track):
    '''Video to sequence'''
    clip.setInPoint(inP, 4)
    clip.setOutPoint(ouP, 4)
    seq.videoTracks[track].insertClip(clip,0)


def agregarvideo(background, clip, whiteclip, seq, inP, ouP):
    '''Custom addVideo, it adds two videos: main and backgruond'''
    addVideo(clip, seq, inP, ouP, track=1) # PRINCIPAL
    if background == 0:
        return
    elif background == 1:
        addVideo(clip, seq, inP, ouP, track=0) # BLUR
    elif background == 2:
        addVideo(whiteclip, seq, inP, ouP, track=0) # WHITE


def agregarblur(clip):
    '''Adds blur effect to background and sets scale effect'''
    qe_project = pymiere.objects.qe.project
    track = qe_project.getActiveSequence().getVideoTrackAt(0)

    for x in range(track.numItems):
        clip = track.getItemAt(x)
        clip.addVideoEffect(qe_project.getVideoEffectByName("Gaussian Blur"))

    time.sleep(1)

    for x in range(0, track.numItems-1):
        clip = pymiere.objects.app.project.activeSequence.videoTracks[0].clips[x]

        for component in clip.components:
            if component.displayName == "Gaussian Blur":
                break
        else:
            raise ValueError("No effect 'Gaussian Blur' found on first clip")

        for property in component.properties:
            if property.displayName == "Blurriness":
                property.setValue(15, True)


        for component in clip.components:
            if component.displayName == "Motion":
                break
        else:
            raise ValueError("No effect 'Motion' found on first clip")

        for property in component.properties:
            if property.displayName == "Scale":
                property.setValue(500, True)



def corregirescala(clip):
    '''Scale effect for main video'''
    qe_project = pymiere.objects.qe.project
    track = qe_project.getActiveSequence().getVideoTrackAt(1)

    for x in range(0, track.numItems-1):
        clip = pymiere.objects.app.project.activeSequence.videoTracks[1].clips[x]

        for component in clip.components:
            if component.displayName == "Motion":
                break
        else:
            raise ValueError("No effect 'Motion' found on first clip")

        for property in component.properties:
            if property.displayName == "Scale":
                property.setValue(185, True)


# %% INPUT
savepath = r'C:\Users\Martin\Downloads\Nueva carpeta'
youtubeurl = r'https://youtu.be/5uQXXkpn6Mk'
adobe_exe= r'C:\Program Files\Adobe\Adobe Premiere Pro 2020\Adobe Premiere Pro.exe'
template_file = r"F:\Codigo\On github\media-python-premiere\adobe-test\Template.prproj"
escala_principal = ""



# %%
descargarvideo(youtubeurl, savepath)
setup(adobe_exe)
abrirproyecto(template_file)
project, items = importvideo(savepath)
listarvideos(items)


# %% ROTAR ENTRE SEQUENCES
sequence_names= ["9:16", "4:5", "1:1", "16:9"]


# %%
clip = items[int(input("Numero: primero va el que queda ultimo, en ultimo lugar va el inicio del video"))]
background = int(input("0 = Black, 1 = Blur, 2 = White"))
whiteclip = [s for s in items if s.name == 'white-background.png'][0]
inpoint = input("Inpoint en segundos")
outpoint = input("Outpoint en segundos")

for sequence in sequence_names:
    sequence_name = sequence
    sequence = [s for s in pymiere.objects.app.project.sequences if s.name == sequence_name][0]
    pymiere.objects.app.project.openSequence(sequenceID=sequence.sequenceID)
    agregarvideo(background,clip,whiteclip,project.activeSequence, inP=inpoint, ouP=outpoint)
    agregarblur(clip)




# %%
qe_project = pymiere.objects.qe.project
track = qe_project.getActiveSequence().getVideoTrackAt(1)

for x in range(0, track.numItems-1):
    clip = pymiere.objects.app.project.activeSequence.videoTracks[1].clips[x]

    for component in clip.components:
        if component.displayName == "Motion":
            break
    else:
        raise ValueError("No effect 'Motion' found on first clip")

    for property in component.properties:
        if property.displayName == "Scale":
            property.setValue(185, True)


# %%
addVideo(items[0], project.activeSequence, 0, 100, 2)
# %%
