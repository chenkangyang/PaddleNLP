# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections
import json
import os

from paddle.dataset.common import md5file
from paddle.utils.download import get_path_from_url
from paddlenlp.utils.env import DATA_HOME
from . import DatasetBuilder

__all__ = ['NLPCC13EVSAM05HIT']


class NLPCC13EVSAM05HIT(DatasetBuilder):
    """
    NLPCC13_EVSAM05_HIT is the dataset for dependency parsing.
    The format of this dataset is based on the CoNLL-X style:

        '''
        raw name        definition 

        ID              Token counter, starting at 1 for each new sentence.
        FORM            Word form or punctuation symbol.
        LEMMA           Lemma or stem (depending on the particular treebank) of word form, or an underscore if not available.
        CPOSTAG         Coarse-grained part-of-speech tag, where the tagset depends on the treebank.
        POSTAG          Fine-grained part-of-speech tag, where the tagset depends on the treebank.
        FEATS           Unordered set of syntactic and/or morphological features (depending on the particular treebank), or an underscore if not available.
        HEAD            Head of the current token, which is either a value of ID, or zero (’0’) if the token links to the virtual root node of the sentence.
        DEPREL          Dependency relation to the HEAD.
        PHEAD           Projective head of current token, which is either a value of ID or zero (’0’), or an underscore if not available.
        PDEPREL         Dependency relation to the PHEAD, or an underscore if not available.
        '''
    """

    URL = 'https://paddlenlp.bj.bcebos.com/datasets/nlpcc13_evsam05_hit.tar.gz'
    MD5 = '5988ede79690dc87aa6e4343b5299944'
    META_INFO = collections.namedtuple('META_INFO', ('file', 'md5'))
    SPLITS = {
        'train': META_INFO(
            os.path.join('nlpcc13_evsam05_hit', 'train.conll'),
            'd82e667950a5e22b18baf595b9feb30f'),
        'dev': META_INFO(
            os.path.join('nlpcc13_evsam05_hit', 'dev.conll'),
            'b71b08dc85e652769bfbda30b1e352a9'),
        'test': META_INFO(
            os.path.join('nlpcc13_evsam05_hit', 'test.conll'),
            '784fb9d966a286df5370f7eee4013cf0'),
    }

    def _get_data(self, mode, **kwargs):
        """Downloads dataset."""
        default_root = os.path.join(DATA_HOME, self.__class__.__name__)
        filename, data_hash = self.SPLITS[mode]
        fullname = os.path.join(default_root, filename)
        if not os.path.exists(fullname) or (data_hash and
                                            not md5file(fullname) == data_hash):
            get_path_from_url(self.URL, default_root, self.MD5)

        return fullname

    def _read(self, filename, split):
        start = 0
        with open(filename, 'r', encoding='utf-8') as f:
            lines = []
            for line in f.readlines():
                if not line.startswith(" "):
                    if not line.startswith('#') and (len(line) == 1 or
                                                     line.split()[0].isdigit()):
                        lines.append(line.strip())
                else:
                    lines.append("")

        for i, line in enumerate(lines):
            if not line:
                values = list(zip(*[j.split('\t') for j in lines[start:i]]))
                if split == "test":
                    ID, FORM, LEMMA, CPOS, POS, FEATS, HEAD, DEPREL = values
                else:
                    ID, FORM, LEMMA, CPOS, POS, FEATS, HEAD, DEPREL, _, _ = values
                if values:
                    yield {
                        "ID": ID,
                        "FORM": FORM,
                        "LEMMA": LEMMA,
                        "CPOS": CPOS,
                        "POS": POS,
                        "FEATS": FEATS,
                        "HEAD": HEAD,
                        "DEPREL": DEPREL,
                    }
                start = i + 1
