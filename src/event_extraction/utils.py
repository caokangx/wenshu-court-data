punctuation = '！，；：？"\'（）.、×“”《》[]!,;:?()-_1234567890\\+-x÷/%#@{}【】／'

def removePunctuation(text):
    for c in punctuation:
        text = text.replace(c, "")
    return text