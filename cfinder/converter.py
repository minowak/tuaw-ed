FNAMES = ['comments-url.csv', 'authors-comments.csv']

def get_lines(fName):
    f = open(fName, encoding="utf8")
    lines = [x.strip('\n') for x in f.readlines()]
    f.close()
    return lines

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    for fName in FNAMES:
        lines = get_lines(fName)
        labels = lines[0].split(';')

        result = ""

        f = open(fName.replace('.csv', '.txt'), 'w', encoding='utf-8')

        line_nr = 1
        for line in lines:
            weight = 0

            i = 0
            entries = line.split(";")
            node1 = entries[0]
            for entry in entries:
                if is_number(entry):
                    weight = float(entry)
                    if weight != 0:
                        node2 = labels[i].replace(' ', '')
                        node1 = node1.replace(' ', '')
                        f.write("\n" + node1 + " " + node2 + " " + str(weight))
                i = i + 1
        line_nr = line_nr + 1

        f.close()
