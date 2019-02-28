import fileinput
from pprint import pprint
from tqdm import tqdm
import numpy as np
from random import shuffle


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
    return photos




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
        self.distances = [[0 for i in range(size)] for i in range(size)]

    def add_distance(self, i, j, d):
        self.distances[i][j] = d;
        self.distances[j][i] = d;

    def get_distance(self, i, j):
        return self.distances[i][j]

    def get_max_distance(self):
        l = len(self.distances)
        max_pos = (0, 0)
        for i in range(l):
            for j in range(l):
                if self.get_distance(max_pos[0], max_pos[1]) < \
                    self.get_distance(i, j):
                    max_pos = (i, j)

        return max_pos




def compute_distances(images):
    distances = Distances(len(images))
    for i, a in enumerate(images):
        for j, b in enumerate(images[i + 1:], start=i + 1):
            distance = tags_distance(a.tags, b.tags)
            distances.add_distance(i, j, distance)

    return distances

def link_chunks(chunk, distances):
    pos = distances.get_max_distance()
    print(pos, distances.get_distance(pos[0], pos[1]))



def main():
    chunk_count = 20

    images = parse()
    # shuffle(images)
    chunk_size = len(images) // chunk_count

    print(chunk_count, chunk_size)
    chunks = [images[i: i + chunk_size] for i in range(0, len(images), chunk_size)]


    print('Computing distances')
    for chunk in tqdm(chunks):
        distances = compute_distances(chunk)
        link_chunks(chunk, distances)
        # pprint(distances.distances)

    # m = get_max(distances)
    # print(distances[m])


if __name__ == "__main__":
    main()
