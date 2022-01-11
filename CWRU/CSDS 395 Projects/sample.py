import webvtt
import speech_recognition as sr
from Mindmap_generation import Text2Mindmap


def get_transcript(file_path):
    vtt = webvtt.read(file_path)
    transcript = ""

    lines = []
    for line in vtt:
        lines.extend(line.text.strip().splitlines())

    previous = None
    for line in lines:
        if line == previous:
            continue
        transcript += " " + line.split(':')[1]
        previous = line

    return transcript


def speech2text(file_path):
    r = sr.Recognizer()

    harvard = sr.AudioFile(file_path)
    with harvard as source:
        audio = r.record(source)

    return r.recognize_sphinx(audio)


def text2mindmap(text, layer_num=2, layer_size=3, leaf_size=1, keyphrases=None):
    # build the model
    t2mm = Text2Mindmap()

    # let the model fit on the text, if adding more parameters if wanted
    t2mm = t2mm.fit(text, layer_num, layer_size, leaf_size, keyphrases)

    # this gives mindmap as a json
    mindmap = t2mm.mindmap

    return mindmap
