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


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions



import os.path as op
from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol, SpeakerRecognitionProtocol
from pyannote.parser import MDTMParser

# this protocol defines a speaker diarization protocol: as such, a few methods
# needs to be defined: trn_iter, dev_iter, and tst_iter.

class LibriSpeechSpeakerRecognitionProtocol(SpeakerDiarizationProtocol):
    """My first speaker diarization protocol """
    
    def __init__(self, preprocessors={}, **kwargs):
        super(LibriSpeechSpeakerRecognitionProtocol, self).__init__(
            preprocessors=preprocessors, **kwargs)
        self.mdtm_parser_ = MDTMParser()


    def _subset(self, protocol, subset):

        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')

        # load annotations
        path = op.join(data_dir, 'librispeech-{protocol}.{subset}.mdtm'.format(subset=subset, protocol=protocol))
        mdtms = self.mdtm_parser_.read(path)

        for uri in sorted(mdtms.uris):
            annotation = mdtms(uri)
            current_file = {
                'database': 'LibriSpeech',
                'uri': uri,
                'annotation': annotation}
            yield current_file




class LibriSpeechClean(LibriSpeechSpeakerRecognitionProtocol):
    """Speaker diarization protocol using `clean` subset of LibriSpeech database"""

    def trn_iter(self):
        return self._subset('clean', 'train')

    def dev_iter(self):
        return self._subset('clean', 'dev')

    def tst_iter(self):
        return self._subset('clean', 'test')



class LibriSpeechOther(LibriSpeechSpeakerRecognitionProtocol):
    """Speaker diarization protocol using `other` subset of LibriSpeech database"""

    def trn_iter(self):
        return self._subset('other', 'train')

    def dev_iter(self):
        return self._subset('other', 'dev')

    def tst_iter(self):
        return self._subset('other', 'test')


class LibriSpeech(Database):
    """LibriSpeech database"""

    def __init__(self, preprocessors={}, **kwargs):
        super(LibriSpeech, self).__init__(preprocessors=preprocessors, **kwargs)

        # register the first protocol: it will be known as
        # MyDatabase.SpeakerDiarization.MyFirstProtocol
        self.register_protocol(
            'SpeakerDiarization', 'LibriSpeechClean', LibriSpeechClean)
        self.register_protocol(
            'SpeakerDiarization', 'LibriSpeechOther', LibriSpeechOther)
