# Author: Till Elton
# hacky and simple, uses python3

# fill me in with what to convert
toconvert = "edible@foo.bar"
# if true, just give encoded string, if false also add formatting in as to suit js document.write
raw = False

entities = {}
i = 33
while (i < 126):
    entities[chr(i)] = ('&#' + str(i) + ';')
    i = i + 1
outstr = ""
for item in toconvert:
    outstr += entities[item]
if raw:
    print(outstr)
    print("/n")

else:
    outstrwithplusses = ""
    for item in outstr:
        outstrwithplusses += ("'" + item + "'+")

    outstrwithplusses = outstrwithplusses[:-1]
    print(outstrwithplusses)
