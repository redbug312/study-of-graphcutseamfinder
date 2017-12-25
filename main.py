#!/usr/bin/python3
import cv2
import numpy as np
import maxflow
import math

intersect = lambda rectA, offA, rectB, offB: tuple(np.subtract(np.minimum(np.add(offA, rectA), np.add(offB, rectB)), np.maximum(offA, offB)))
union     = lambda rectA, offA, rectB, offB: tuple(np.subtract(np.maximum(np.add(offA, rectA), np.add(offB, rectB)), np.minimum(offA, offB)))


def new_patch(image, patch, offset, show_cut):
    overlap_y, overlap_x = intersect(image.shape, (0, 0), patch.shape, offset)
    image_overlap = image[offset[0]:offset[0]+overlap_y, offset[1]:offset[1]+overlap_x]
    patch_overlap = patch[:overlap_y, :overlap_x]

    g = maxflow.Graph[float]()
    nodes = g.add_grid_nodes((overlap_y, overlap_x))

    # edges between overlap and source/sink
    source, sink = (math.inf, 0), (0, math.inf)
    g.add_grid_tedges(nodes[1:, -1], *sink)     # right-bottom
    g.add_grid_tedges(nodes[-1,:-1], *sink)     # bottom-left
    g.add_grid_tedges(nodes[:-1, 0], *source)   # left-top
    g.add_grid_tedges(nodes[0,  1:], *source)   # top-right

    # edges in overlap, right and down respectively
    norm = np.abs(image_overlap.astype(float) - patch_overlap.astype(float)) / 256
    g.add_grid_edges(nodes, weights=(norm + np.roll(norm, -1, axis=1)), structure=np.array([[0, 0, 1]])  , symmetric=True)
    g.add_grid_edges(nodes, weights=(norm + np.roll(norm, -1, axis=0)), structure=np.array([[0, 0, 1]]).T, symmetric=True)

    flow = g.maxflow()
    print('maxflow: {}'.format(flow))

    # min-cut would divide the graph into two parts
    segments = g.get_grid_segments(nodes)
    overlap = np.where(segments, patch_overlap, image_overlap)
    if show_cut:
        cut = np.logical_or.reduce([np.logical_xor(segments, np.roll(segments,  1, axis=0)),
                                    np.logical_xor(segments, np.roll(segments,  1, axis=1)),
                                    np.logical_xor(segments, np.roll(segments, -1, axis=0)),
                                    np.logical_xor(segments, np.roll(segments, -1, axis=1))])
        cut[:, :1] = cut[:1, :] = cut[:, -1:] = cut[-1:, :] = False
        overlap = np.where(cut, [[0]], overlap)

    # copy the old image, patch, overlap to a new one
    result = np.ndarray(union(image.shape, (0, 0), patch.shape, offset))
    result[         :              image.shape[0],          :              image.shape[1]] = image[:, :]
    result[offset[0]:offset[0] +   patch.shape[0], offset[1]:offset[1] +   patch.shape[1]] = patch[:, :]
    result[offset[0]:offset[0] + overlap.shape[0], offset[1]:offset[1] + overlap.shape[1]] = overlap[:, :]
    return result.astype(np.uint8)


def main(args):
    image = cv2.imread(args.image, 0)
    patch = np.copy(image)

    image = new_patch(image, patch, (400, 100), args.cut)
    image = new_patch(image, patch, (200, 600), args.cut)

    cv2.imshow("Result", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Image Synthesis with graph cut')
    parser.add_argument('image', metavar='IMAGE', help='original image to synthesis')
    parser.add_argument('-c', '--cut', action='store_true', help='show the minimum cut')
    main(parser.parse_args())
