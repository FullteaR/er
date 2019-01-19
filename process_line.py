import re
import sys
date = re.compile("^\d{4}/\d{2}/\d{2}\([月火水木金土日]\)$")
phone = re.compile("^☎ 不在着信$|^☎ 通話時間 [\d:]+$")  # 雑?


def line(opponent):
    talk = open("./data/[LINE] {}とのトーク.txt".format(opponent), "r")
    contents = talk.readlines()[2::]
    talk.close()
    contents = [content.strip() for content in contents if (
        date.match(content) == None and content != "\n")]
    contents_remove_kaigyou = []
    text = ""
    for content in contents:
        if "\t" in content:
            contents_remove_kaigyou.append(text)
            text = content
        else:
            text += content

    contents_remove_kaigyou.append(text)
    contents_remove_kaigyou.pop(0)
    retval = []
    speaker = None
    text = ""
    for content_remove_kaigyou in contents_remove_kaigyou:
        data = content_remove_kaigyou.split("\t")
        if len(data) < 3:
            continue
        _speaker = data[1]
        content = data[2]
        if content == "[写真]" or content == "[スタンプ]" or phone.match(content):
            continue
        if speaker == _speaker:
            text += " " + content
        else:
            speaker = _speaker
            text=text.replace("\"","")
            retval.append(text)
            text = speaker + "\t" + content
    retval.append(text)
    retval.pop(0)
    return retval


if __name__ == "__main__":
    name = " ".join(sys.argv[1::])
    talk = line(name)
    with open("./data/line.txt", "w") as fp:
        fp.writelines("\n".join(talk))
    with open("./data/corpus.txt", "a") as fp:
        for i in talk:
            if i.split("\t")[0] == name:
                fp.write(i.split("\t")[1])
                fp.write("\n")
