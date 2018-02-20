#!/usr/bin/env python
'''
Linear frame interpolation using Bidirectional Block-Based Motion Compensation
'''
import argparse

if __name__ == "__main__":

    #Define args parser and args
    parser = argparse.ArgumentParser(description='Block-based time-domain motion estimation.')
    parser.add_argument('-b', type=int, default=32,
                        help='block_size: Size of the blocks in the motion estimation process (Integer) (Default value: 32)')
    parser.add_argument('-d', type=int, default=0,
                        help='bordder_size: Size of the border of the blocks in the motion estimation process (Integer) (Default value: 0)')
    parser.add_argument('-e', type=str, default="even",
                        help='even_fn: Input file with the even pictures (String) (Default value: "even")')
    parser.add_argument('-i', type=str, default="imotion",
                        help='imotion_fn: Input file with the initial motion fields (String) (Default value: "imotion")')
    parser.add_argument('-m', type=str, default="motion",
                        help='motion_fn: Output file with the motion fields (String) (Default value: "motion")')
    parser.add_argument('-o', type=str, default="odd",
                        help='odd_fn: Input file with odd pictures (String) (Default value: "odd")')
    parser.add_argument('-p', type=int, default=9,
                        help='pictures: Number of images to process (Integer) (Default value: 9)')
    parser.add_argument('-x', type=int, default=352,
                        help='pixels_in_x: Size of the X dimension of the pictures (Integer) (Default value: 352)')
    parser.add_argument('-y', type=int, default=288,
                        help='pixels_in_y: Size of the Y dimension of the pictures (Integer) (Default value: 288)')
    parser.add_argument('-s', type=int, default=4,
                        help='search_range: Size of the searching area of the motion estimation (Integer) (Default value: 4)')
    parser.add_argument('-a', type=int, default=0,
                        help='subpixel_accuracy: Sub-pixel accuracy of the motion estimation (Integer) (Default value: 0)')

    #Parse args
    args = parser.parse_args()

    block_size = args.b
    border_size = args.d
    even_fn = args.e
    imotion_fn = args.i
    motion_fn = args.m
    odd_fn = args.o
    pictures = args.p
    pixels_in_x = args.x
    pixels_in_y = args.y
    search_range = args.s
    subpixel_accuracy = args.a

    #DO STUFF