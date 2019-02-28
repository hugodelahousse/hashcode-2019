import fileinput
from pprint import pprint
from tqdm import tqdm
import numpy as np
from random import shuffle


def parse():
    lines = [line.strip() for line in fileinput.input()]
    count = int(lines[0])
    lines = lines[1:]

    portraits = []
    photos = []

    for i, line in enumerate(lines):
        data = line.split(' ')

        if data[0] == 'V':
            portraits.append(
                Photo(
                    i,
                    data[0] == 'V',
                    set(map(tag_transform, data[2:])),
                )
            )
        else:
            photos.append(
                Photo(
                    i,
                    data[0] == 'V',
                    set(map(tag_transform, data[2:])),
                )
            )
    return photos, portraits




class Photo:
    def __init__(self, index, portrait, tags):
        self.index = index
        self.portrait = portrait
        self.tags = tags

    def __repr__(self):
        return f'<Photo {self.portrait} [{self.tags}]>'

    def get_output(self):
        if isinstance(self.index, int):
            return self.index
        return f'{self.index[0]} {self.index[1]}'


TAGS = {}
def tag_transform(tag):
    value = TAGS.get(tag)
    if value is not None:
        return value
    value = len(TAGS)
    TAGS[tag] = value
    return value

def tags_distance(a, b):
    inter = len(a & b)
    return min(
        inter,
        len(a) - inter,
        len(b) - inter,
    )



class Distances:
    def __init__(self, size):
        self.distances = np.zeros((size, size), dtype=np.int8)

    def get_distance(self, i, j):
        return self.distances[i][j]

    def add_distance(self, i, j, d):
        self.distances[i][j] = d;
        self.distances[j][i] = d;

    def get_max_distance(self):
        max_pos = np.unravel_index(np.argmax(self.distances, axis=None), self.distances.shape)
        return max_pos

    def remove_couple(self, i, j):
        self.distances[:,i] = -1
        self.distances[:j,] = -1

def compute_distances(images):
    distances = Distances(len(images))
    for i, a in enumerate(images):
        for j, b in enumerate(images[i + 1:], start=i + 1):
            distance = tags_distance(a.tags, b.tags)
            distances.add_distance(i, j, distance)

    return distances

def link_chunks(chunk, distances):
    sorted_images = []

    pos = distances.get_max_distance()


    print(pos, distances.get_distance(pos[0], pos[1]))



def main():
    chunk_count = 23

    images, portraits = parse()

    portraits.sort(reverse=True, key=lambda p: len(p.tags))

    for i in range(0, len(portraits), 2):
        images.append(Photo((portraits[i].index, portraits[i+1].index), True,
            portraits[i].data + portraits[i+1].data))

    shuffle(images)
    chunk_size = len(images) // chunk_count

    print(chunk_count, chunk_size)
    chunks = [images[i: i + chunk_size] for i in range(0, len(images), chunk_size)]

    assert(len(images) == sum(len(chunk) for chunk in chunks))

    print('Computing distances')
    for chunk in tqdm(chunks):
        distances = compute_distances(chunk)
        link_chunks(chunk, distances)
        # pprint(distances.distances)

    # m = get_max(distances)
    # print(distances[m])


if __name__ == "__main__":
    main()
