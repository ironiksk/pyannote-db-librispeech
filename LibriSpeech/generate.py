#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Olexandr Korniienko


import fnmatch
import glob
import os.path
import sys

from subprocess import call

from pyannote.audio.features.utils import get_wav_duration

CONCATENATE = True

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ... %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben

def file2wav(inp, out):
    cmd = 'ffmpeg -n -i {inp} -ar 16000 {out}.wav > /dev/null 2> /dev/null'.format(
            inp = inp, out = out)
    call(cmd, shell=True)

def list2wav(inp, out):
    cmd = 'ffmpeg -n -f concat -safe 0 -i {} -c copy -ab 160k -ar 16000 -vn {}.wav  > /dev/null 2> /dev/null'.format(inp, out)
    # print cmd
    call(cmd, shell=True)


def listdir_nohidden(path):
    files = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            files.append( f)
    return files




def init_database(db_dir, protocols, annotation_dir, path_to_wav):
    """Create annotation files for datasets

    Parameters
    ----------
    db_dir : string
        Path where SPEAKERS.txt exists (path to LibriSpeech filedir)
    protocols : list of strings
        List of strings with protocols like ['dev-clean', 'dev-other', ...]
    annotation_dir: string
        Path to annotation files
    path_to_wav : string
        Path where wav files created. This string should put to ~/.pyannote/db.yaml

    Usage
    -----

    """

    # wav_path_template = '{db_dir}/wav/{subset}/{uri}'
    wav_path_template = '{path_to_wav}/{uri}'

    # read file descriptor
    desc = {}
    with open(os.path.join(db_dir, 'SPEAKERS.TXT'), 'r') as file:
        content = file.readlines()
        for c in content:
            fields = c.translate(None, '\' -()\n').split('|')
            # fields = c.translate('\' -()\n').split('|')
            if fields[0][0] == ';':
                continue
            desc[fields[0]] = {
                'gender': 'male' if fields[1] == 'M' else 'female',
                'subset': fields[2],
                'duration': float(fields[3]),
                'client_id': fields[4]
            }

    for protocol in protocols:

        filedir = os.path.join(db_dir, protocol)

        subset = 'librispeech-{}.{}'.format(protocol.split('-')[1], protocol.split('-')[0])
        try:
            # os.makedirs(wav_path_template.format(db_dir = db_dir, subset = subset, uri=''))
            os.makedirs(wav_path_template.format(path_to_wav = path_to_wav, uri=''))
        except:
            print ('Directory exists')

        clients = listdir_nohidden(filedir)
        clients.sort(key=lambda a: a.lower())

        n_clients = len(clients)
        counter = 0

        for c in clients:
            d = desc[c]

            progress(counter, n_clients, d['client_id'])
            counter += 1

            group_sample_path = os.path.join(filedir, c)
            books = listdir_nohidden(group_sample_path)
            for b in books:
                books_sample_path = os.path.join(group_sample_path, b)
                files = listdir_nohidden(books_sample_path)

                if not CONCATENATE:
                    for f in files:
                        flac_sample_path = os.path.join(books_sample_path, f)
                        if flac_sample_path.endswith(".flac"):
                            # sample_path = wav_path_template.format(
                            #     uri = os.path.splitext(flac_sample_path)[0].split('/')[-1],
                            #     subset = subset,
                            #     db_dir = db_dir
                            # )
                            sample_path = wav_path_template.format(
                                uri = os.path.splitext(flac_sample_path)[0].split('/')[-1],
                                path_to_wav = path_to_wav
                            )

                            if not os.path.exists(sample_path + '.wav'):
                                file2wav(flac_sample_path, sample_path)


                            with open(os.path.join(annotation_dir, 'data', subset + '.mdtm'), 'a') as datafile:
                                datafile.write('{uri} {channel} {start} {duration} {modality} {confidence} {gender} {label}\n'.format(
                                    uri = os.path.splitext(flac_sample_path)[0].split('/')[-1],
                                    channel = 1,
                                    start = 0,
                                    duration = get_wav_duration(sample_path + '.wav'),
                                    modality = 'speaker',
                                    confidence = 'NA',
                                    gender = d['gender'],
                                    label = d['client_id']
                                ))

                else:
                    
                    fname = "list.txt"
                    with open(fname, 'a') as file:
                        for f in files:
                            flac_sample_path = os.path.join(books_sample_path, f)
                            if flac_sample_path.endswith(".flac"):
                                file2wav(flac_sample_path, os.path.splitext(flac_sample_path)[0])
                                file.write("file \'{}\'\n".format(os.path.splitext(flac_sample_path)[0]+'.wav'))

                    # sample_path = wav_path_template.format(
                    #     uri = '{}-{}-{}'.format(c, d['client_id'], b),
                    #     subset = subset,
                    #     db_dir = db_dir
                    # )
                    sample_path = wav_path_template.format(
                        uri = '{}-{}-{}'.format(c, d['client_id'], b),
                        path_to_wav = path_to_wav
                    )

                    if not os.path.exists(sample_path + '.wav'):
                        list2wav(fname, sample_path)
                    os.remove(fname)


                    with open(os.path.join(annotation_dir, 'data', subset + '.mdtm'), 'a') as datafile:
                        datafile.write('{uri} {channel} {start} {duration} {modality} {confidence} {gender} {label}\n'.format(
                            uri = sample_path.split('/')[-1],
                            channel = 1,
                            start = 0,
                            duration = get_wav_duration(sample_path + '.wav'),
                            modality = 'speaker',
                            confidence = 'NA',
                            gender = d['gender'],
                            label = d['client_id']
                        ))                    



if __name__ == '__main__':
    init_database('/path/to/corpus/LibriSpeech', ['dev-clean', 'test-clean', 'train-clean'], '/path/to/cloned/pyannote-db-librispeech/LibriSpeech', '/path/to/corpus/LibriSpeech/wav')
    