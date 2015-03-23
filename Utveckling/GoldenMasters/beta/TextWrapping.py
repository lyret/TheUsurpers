#Made by: Unknown, taken from the pygame wiki's article on text wrapping
from itertools import chain



#Wraps a text to a constraint set. font is a pygame font object
def wrapline(text, font, maxwidth):
    done=0
    wrapped=[]
    
    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text=text[nl:]
    return wrapped


#Wraps a text and takes \n into account.
def wrap_multi_line(text, font, maxwidth):
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)






#Private function
def truncline(text, font, maxwidth):
    real=len(text)
    stext=text
    l=font.size(text)[0]
    cut=0
    a=0
    done=1
    old = None
    while l > maxwidth:
        a=a+1
        n=text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext= n[:-cut]
        else:
            stext = n
        l=font.size(stext)[0]
        real=len(stext)
        done=0
    return real, done, stext