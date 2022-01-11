import re
from nltk.tokenize import sent_tokenize
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer, util
import yake

nlp = spacy.load("en_core_web_sm")
roberta = SentenceTransformer('stsb-roberta-large')
extractor = yake.KeywordExtractor(lan='en', n=3, dedupLim=0.9, dedupFunc='seqm', top=20)

color_arr = ['#5B8FF9', '#DECFEA', '#FBC530', '#FD603C', '#17C252']


class Text2Mindmap():

    def __init__(self, d=0.85, alpha=0.5):
        self.d = d
        self.alpha = alpha

    def prepare_sents(self, text):
        """prepare the text into sents
        This method parses the transcript into individual sentence and encode sentence to vector.
        The embedded sentences are stored in embedded_sents list and the sentence number are stored in sent_nums.
        Args:
            text (String): original transcript from lecture
        """
        self.raw_sents = []
        self.embedded_sents = []
        for sent in sent_tokenize(text):
            self.raw_sents.append(sent)
            token_list = []
            for token in nlp(sent):
                word = re.sub('[\W]+', ' ', token.lemma_.lower())
                if word != ' ':
                    token_list.append(word)
            sent = ' '.join(token_list)
            self.embedded_sents.append(roberta.encode(sent, convert_to_tensor=True))
        self.sent_nums = len(self.embedded_sents)

    def extract_keyphrases(self, keyphrases):
        """[extract all keyphrases from original transcript]
        Based on the layer number and layer size, this method extracts keyphrases within each layer.
        Extracted keyphrases are stored in raw_kephrases and embedded_keyphrases list.
        For each keyphrase, its leaf has the index layer_size x (index+1)
        Args:
            keyphrases (String list): keyphrases that the users provide
        """
        self.raw_keyphrases = []
        self.embedded_keyphrases = []
        self.keyphrase_sentence = {'root': [i for i in range(self.sent_nums)]}

        for i in range(self.layer_num):
            if i == 0:
                parent_keyphrases = ['root']
            elif i == 1:
                if keyphrases:
                    self.raw_keyphrases.extend(keyphrases)
                    self.embedded_keyphrases.extend([roberta.encode(keyphrase, convert_to_tensor=True) for keyphrase in keyphrases])
                if not keyphrases or len(keyphrases) != self.layer_size:
                    sub_text = ' '
                    for j in self.keyphrase_sentence['root']:
                        sub_text = sub_text + ' ' + self.raw_sents[j]
                    keywords_wd = extractor.extract_keywords(sub_text)
                    keywords = [roberta.encode(x, convert_to_tensor=True) for x, _ in keywords_wd]
                    index = 1
                    if not keyphrases:
                        count = 0
                    else:
                        count = len(keyphrases) 
                    while count < self.layer_size:
                        is_overlapped = False
                        for found_keyphrase in self.embedded_keyphrases:
                            if cos_similarity(keywords[index], found_keyphrase) > 0.6:
                                is_overlapped = True
                                break
                        if not is_overlapped:
                            self.embedded_keyphrases.append(keywords[index])
                            self.raw_keyphrases.append(keywords_wd[index][0])
                            count += 1
                        index += 1
                count = 0
                for sent_ids in self.keyphrase_sentence['root']:
                    closest_id = find_closest(self.embedded_sents[sent_ids], self.embedded_keyphrases[-self.layer_size:])
                    keyphrase = self.raw_keyphrases[closest_id + len(self.embedded_keyphrases) - self.layer_size]
                    if keyphrase in self.keyphrase_sentence.keys():
                        temp = self.keyphrase_sentence[keyphrase]
                        temp.append(sent_ids)
                        self.keyphrase_sentence[keyphrase] = temp
                    else:
                        self.keyphrase_sentence[keyphrase] = [sent_ids]
                    count += 1
            else:
                parent_keyphrases = self.raw_keyphrases[-self.layer_size ** i:]

                for parent_keyphrase in parent_keyphrases:
                    sub_text = ' '
                    for j in self.keyphrase_sentence[parent_keyphrase]:
                        sub_text = sub_text + ' ' + self.raw_sents[j]
                    keywords_wd = extractor.extract_keywords(sub_text)
                    keywords = [roberta.encode(x, convert_to_tensor=True) for x, _ in keywords_wd]
                    index = 0
                    while keywords_wd[index][0] == parent_keyphrase:
                        index += 1
                    self.raw_keyphrases.append(keywords_wd[index][0])
                    self.embedded_keyphrases.append(keywords[index])
                    index += 1
                    count = 1
                    while count < self.layer_size:
                        is_overlapped = False
                        for found_keyphrase in self.embedded_keyphrases:
                            if cos_similarity(keywords[index], found_keyphrase) > 0.7:
                                is_overlapped = True
                                break
                        if not is_overlapped:
                            self.embedded_keyphrases.append(keywords[index])
                            self.raw_keyphrases.append(keywords_wd[index][0])
                            count += 1
                        index += 1

                    count = 0
                    for sent_ids in self.keyphrase_sentence[parent_keyphrase]:
                        closest_id = find_closest(self.embedded_sents[sent_ids], self.embedded_keyphrases[-self.layer_size:])
                        keyphrase = self.raw_keyphrases[closest_id + len(self.embedded_keyphrases) - self.layer_size]
                        if keyphrase in self.keyphrase_sentence.keys():
                            temp = self.keyphrase_sentence[keyphrase]
                            temp.append(sent_ids)
                            self.keyphrase_sentence[keyphrase] = temp
                        else:
                            self.keyphrase_sentence[keyphrase] = [sent_ids]
                        count += 1

    def calc_similarity(self, sent1, sent2):
        """calculate similarity between two sentences
        This method calculates similarity between two sentences based on layer similarity and cosine similarity.
        Args:
            sent1 (int): sent 1 index
            sent2 (int): sent 2 index
        """
        score = self.alpha * cos_similarity(self.embedded_sents[sent1], self.embedded_sents[sent2])
        index = 0
        for i in range(self.layer_num - 1):
            for index in range(index, index + self.layer_size ** (i + 1)):
                if sent1 in self.keyphrase_sentence[self.raw_keyphrases[index]]:
                    sent1_kw_id = index
                if sent2 in self.keyphrase_sentence[self.raw_keyphrases[index]]:
                    sent2_kw_id = index
            index += 1
            score += pow(1 - self.alpha, self.layer_num - i - 2) * cos_similarity(self.embedded_sents[sent1_kw_id], self.embedded_sents[sent2_kw_id])
        return score

    def score(self):
        """
        use TextRank algorithm to calculate the score of each sentence
        """
        self.simi_matrix = np.zeros([self.sent_nums, self.sent_nums])
        for i in range(self.sent_nums):
            for j in range(self.sent_nums):
                if i < j:
                    self.simi_matrix[i][j] = self.calc_similarity(i, j)
                elif i > j:
                    self.simi_matrix[i][j] = self.simi_matrix[j][i]
        median = np.median(self.simi_matrix)
        for i in range(self.sent_nums):
            for j in range(self.sent_nums):
                if self.simi_matrix[i][j] < median:
                    self.simi_matrix[i][j] = 0
        sent_simi_sums = [sum(self.simi_matrix[:, i]) for i in range(self.sent_nums)]
        self.simi_matrix = self.simi_matrix / sent_simi_sums

        self.scores = np.ones([self.sent_nums, ])
        for _ in range(50):
            self.scores = (1 - self.d) + self.d * np.dot(self.simi_matrix, self.scores)

    def put_children_keyphrases(self, parent_index, layer, id):
        children = []
        if parent_index == -1 and layer == 1:
            for i in range(self.layer_size):
                child = {}
                child['label'] = self.mindlist[i]
                child['id'] = id + '-' + str(i + 1)
                child['color'] = color_arr[i]
                child['children'] = self.put_children_keyphrases(i, layer + 1, child['id'])
                children.append(child)
            return children
        # middle keyphrases
        elif layer < self.layer_num:
            child_begin = self.layer_size * (parent_index + 1)
            child_end = child_begin + self.layer_size
            size_count = 1
            for i in range(child_begin, child_end):
                child = {}
                child['label'] = self.mindlist[i]
                child['id'] = id + '-' + str(size_count)
                child['children'] = self.put_children_keyphrases(i, layer + 1, child['id'])
                size_count += 1
                children.append(child)
            return children
        # last sentence layer
        else:
            last_keyphrase_count = self.layer_size**(self.layer_num - 1)
            child_index = parent_index + last_keyphrase_count
            # print(child_index)
            sentences = self.mindlist[child_index]
            for i in range(self.leaf_size):
                child = {}
                child['label'] = sentences[i]
                child['id'] = id + '-' + str(i + 1)
                children.append(child)
            return children

    def rebuild(self):
        self.mindmap = {}
        self.mindmap['label'] = 'MindMap'
        self.mindmap['id'] = '0'
        self.mindmap['children'] = self.put_children_keyphrases(-1, 1, '0')

    def generate_mindmap(self):
        """
        generate the mindmap by selecting the sentences with the first several highest score in each cluster
        """
        self.mindlist = self.raw_keyphrases.copy()

        for last_keyphrase in self.raw_keyphrases[-self.layer_size ** (self.layer_num - 1):]:
            sent_ids = self.keyphrase_sentence[last_keyphrase]
            sorted_pair = sorted(((self.scores[index], self.raw_sents[index]) for index in sent_ids), reverse=True)
            self.mindlist.append([i[1] for i in sorted_pair[:self.leaf_size]])

        self.rebuild()

    def fit(self, text, layer_num, layer_size, leaf_size, keyphrases):
        """main function that runs the model
        This method is the main caller method that runs the model.
        Args:
            layer_num (int): number of layer in mindmap
            layer_size (int): number of keyword in one layer
            leaf_size (int): number of sentence for each keyphrase
            keyphrases (String list): keyphrases user provides
        """
        self.layer_num = layer_num
        self.layer_size = layer_size
        self.leaf_size = leaf_size

        self.prepare_sents(text)
        self.extract_keyphrases(keyphrases)
        self.score()
        self.generate_mindmap()
        return self


def cos_similarity(sent1, sent2):
    """calculate similarity between two sentences
    This method calculates cosine similarity between two sentence vectors.
    Args:
        sent1 (vector): sent 1
        sent2 (vector): sent 2
    Returns:
        score: similarity score
    """
    similarity = util.pytorch_cos_sim(sent1, sent2)
    return similarity.item()


def find_closest(sent, keyphrases):
    """
    find the sentence's closest keyphrase
    Args:
        sent (vector): sentence
        keyphrases (vector list): keyphrases
    Returns:
        list: sorted keyphrase list based on similarity
    """
    return sorted(((cos_similarity(sent, keyphrases[i]), i) for i in range(len(keyphrases))), reverse=True)[0][1]
