# -*- coding: utf-8 -*-
# /usr/bin/python2

import glob
import random

from tensorpack.dataflow.base import RNGDataFlow
from tensorpack.dataflow.common import BatchData
from tensorpack.dataflow import PrefetchData

from audio import read_wav, wav2melspec_db, trim_wav, fix_length
from hparam import hparam as hp
import numpy as np


class DataFlow(RNGDataFlow):
    def __init__(self, data_path, batch_size):
        self.batch_size = batch_size
        self.wav_files = glob.glob(data_path)

    def __call__(self, n_prefetch=1000, n_thread=1):
        df = self
        df = BatchData(df, self.batch_size)
        df = PrefetchData(df, n_prefetch, n_thread)
        return df

    def get_data(self):
        while True:
            wav_file = random.choice(self.wav_files)
            yield get_wav_and_melspec(wav_file)


def get_wav_and_melspec(wav_file):
    wav = read_wav(wav_file, sr=hp.signal.sr)
    wav = trim_wav(wav)
    wav = fix_length(wav, hp.signal.max_length)

    melspec = wav2melspec_db(wav, sr=hp.signal.sr, n_fft=hp.signal.n_fft, win_length=hp.signal.win_length,
                             hop_length=hp.signal.hop_length, n_mels=hp.signal.n_mels,
                             min_db=hp.signal.min_db, max_db=hp.signal.max_db)
    wav = np.expand_dims(wav, -1)
    return wav, melspec
