import fileinput

def parse():
    lines = [line.strip() for line in fileinput.input()]
    count = int(lines[0])
    lines = lines[1:]

    photos = []

    for line in lines:
        data = line.split(' ')

        photos.append(
            Photo(
                data[0] == 'V',
                set(map(tag_transform, data[2:])),
            )
        )
    print(photos)




class Photo:
    def __init__(self, portrait, tags):
        self.portrait = portrait
        self.tags = tags

    def __repr__(self):
        return f'<Photo {self.portrait} [{self.tags}]>'


TAGS = {}
def tag_transform(tag):
    value = TAGS.get(tag)
    if value is not None:
        return value
    value = len(TAGS)
    TAGS[value] = tag
    return value

def tags_distance(a, b):
    return min(
        len(a & b),
        len(a - b),
        len(b - a),
    )


if __name__ == "__main__":
    parse()
