from seq2seq.models import SimpleSeq2Seq, AttentionSeq2Seq
import keras
import MeCab
from gensim.models import word2vec
import re
import numpy as np
from process_wiki import han2zen, zen2han, m

model_wv = word2vec.Word2Vec.load("./model/wiki.model")

url = re.compile(r"http(s)?://([\w\-]+\.)+[\w\-]+(\/[\w\- ./?%&=]*)?")


def line2vec(text, length=20):
    # 記号類
    text = re.sub("[！!]+", "!", text)
    text = re.sub("[？?]+", "?", text)
    text = zen2han(text, kana=False)
    text = han2zen(text, ascii_=False, digit=False, kakko=False)
    text = re.sub("\d+", "0", text)
    text = text.lower()
    text = re.sub("w+", "w", text)
    text = url.sub("", text)
    text = text.replace("[ファイル]", "")

    # OLK特有の固有名詞、他
    text = text.replace("olk", "オリエンテーリング サークル")
    text = text.replace("メンブレ", "メンタル ブレイク")
    text = text.replace("ブリケ", "ストレージ")
    text = re.sub("オリエンテーリング|オリエン", "オリエンテーリング", text)
    text = text.replace("スクショ", "スクリーンショット")
    text = text.replace("追いコン", "追い出し コンパ")

    # 人名#この置換処理は個人情報保護の観点から記載していません。

    
    parsed = m.parse(text).strip().split(" ")

    vector = [model_wv[p] for p in parsed if p in model_wv]
    if length:
        if length < len(vector):
            vector = vector[len(vector) - length::]
        else:
            for _ in range(length - len(vector)):
                vector.append(model_wv["。"])
    return vector


def vec2line(vector):
    text = ""
    for v in vector:
        text += model_wv.most_similar([v], [], 1)[0][0]
    return text


model = AttentionSeq2Seq(input_dim=200,input_length=20, output_length=20, output_dim=200)
model.compile(loss='mse', optimizer='Adam')
model.load_weights("./data/er.hdf5")
def talk(text):
  vector=np.asarray(line2vec(text,length=20)[::-1])
  vector=vector.reshape(1,20,200)
  predict=model.predict(vector,batch_size=132)
  return vec2line(predict.reshape(20,200))



if __name__=="__main__":
    while True:
        print(talk(input(">")))
