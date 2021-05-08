import speech_recognition as sr
from pydub import AudioSegment
import json
from scipy.io import wavfile
import sys
import os
from punctuator import Punctuator
import re
import pickle
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import torch
corpus=""

def overlapping_intervals(arr, overlap_padding, len_interval):
    all_intervals = []
    i = 0
    start = 0
    end = start + len_interval
    if end > arr[1]:
        # print("{} => {}".format(arr[0], arr[1]))
        all_intervals.append([arr[0], arr[1]])
    while True:
        if end > arr[1]:
            # print("{} => {}".format(start, arr[1]))
            all_intervals.append([start, arr[1]])
            break
        # print("{} => {}".format(start, end))
        all_intervals.append([start, end])
        start = start + len_interval - overlap_padding
        end = start + len_interval
    return all_intervals        

def get_transcriptions(audio_file_path, intervals):
    global corpus
    # print("Generating transcripts ...")
    r = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_file_path)
    
    speakers = {'0': {'time_stamps': [], 'transcripts':[]}}

    for i in range(len(intervals)):
        audio = AudioSegment.from_wav(audio_file_path)
        part_audio = audio[intervals[i][0] * 1000 : intervals[i][1] * 1000]
        part_audio.export('temp.wav', format="wav") #Exports to a wav file in the current path.
        
        file = sr.AudioFile("temp.wav")
        # print(round((intervals[i][0]/300)*100),"% done")
        #sys.stdout.flush()
        with file as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
        # Google Speech Recognition
        
        try:
            recog = r.recognize_google(audio, language = 'en-GB')
            
            #print("Duration => {}s to {}s\nTranscription => {}\n".format(intervals[i][0], intervals[i][1], recog))            
            speakers['0']['time_stamps'].append([intervals[i][0], intervals[i][1]])
            speakers['0']['transcripts'].append(recog)
            corpus+=" "+recog

        except sr.UnknownValueError:
            recog = "Google Speech Recognition could not understand audio"
            
            speakers['0']['time_stamps'].append([intervals[i][0], intervals[i][1]])
            speakers['0']['transcripts'].append(recog)

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
    print("Done Transcription! \n")    
    return speakers
    

def convert_to_wav(src):
    #Convert MP3 to WAV
    base_name = os.path.basename(os.path.join("uploads",src))
    print("\n\n\nBASENAME: ",base_name)
    base_name = base_name.split(".")[0] + ".wav"
    print("\n\n\nBASENAME: ",base_name)
    print("\n\n\nBASENAME: ",os.path.join("uploads",src))
    sound = AudioSegment.from_file('2464345179.mp4', "mp4")
    sound.export(os.path.join("uploads",base_name), format="wav")
    return base_name

def extractive(text):
    print("Performing extractive summarization .... \n\n")
    modelfile = './models/bert_model.pickle'
    model = pickle.load(open(modelfile, 'rb'))
    summary = model(text, ratio=0.6)
    return summary
    # print("Extractive summary is: \n")
    # print(summary)
    # print("\n\n")
    

def abstractive(text):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')
    t5_prepared_Text = "summarize: "+text
    # print ("original text preprocessed: \n", preprocess_text)

    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

    # summmarize 
    summary_ids = model.generate(tokenized_text,
                                num_beams=4,
                                no_repeat_ngram_size=2,
                                min_length=30,
                                max_length=100,
                                early_stopping=True)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output

def fix_result(text):
    result=[i.strip().capitalize() for i in text.split(".") ]
    return result

def abstractive_sum(text):
    result=""
    n=len(text)
    print("Performing extractive summarization .... \n\n")
    i=0
    k=1001
    while(i<n):
        if(i+k>n):
            temp=abstractive(text[i:n])
        else: 
            temp=abstractive(text[i:i+k])
        i=i+k
        result+=temp
        
    result=fix_result(result)
    result=".".join(result)
    return result
    # print("Abstractive summary is: \n")
    # print(result)
    # print("\n\n")

    
def punctuate_text(text):
    print("Performing Puntuation ... \n")
    p = Punctuator('models/punctuator1.pcl')
    new_text=p.punctuate(text)
    new_text = re.sub("[?:;,]", "", new_text)
    new_text = re.sub("\s\s+", " ", new_text)
    print("Original text is:\n")
    print(new_text)
    print("\n\n")
    return new_text
    
if __name__ == "__main__":
    samplerate, data = wavfile.read('./clips/lec1.wav')
    rduration = len(data) / samplerate
    #print(f"duration = {duration}")'
    duration=0
    if(rduration>300):duration=300
    else:duration=rduration

    print(f"duration = {duration}s")
    all_intervals = overlapping_intervals([0, duration], 1, 15)
    data = get_transcriptions('./clips/lec1.wav', all_intervals)
    text=punctuate_text(corpus)
    extractive(text)
    abstractive_sum(text)

