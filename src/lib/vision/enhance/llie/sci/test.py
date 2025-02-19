#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/vis-opt-group/SCI

from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np
import torch
import torch.utils
import torchvision
from PIL import Image
from torch.autograd import Variable

import mon
from model import Finetunemodel
from multi_read_data import MemoryFriendlyLoader

console = mon.console


def save_images(tensor, path):
    image_numpy = tensor[0].cpu().float().numpy()
    image_numpy = (np.transpose(image_numpy, (1, 2, 0)))
    im = Image.fromarray(np.clip(image_numpy * 255.0, 0, 255.0).astype("uint8"))
    im.save(path, "png")


def test(args):
    console.log(f"Data: {args.data}")

    if not torch.cuda.is_available():
        console.log("No gpu device available")
        sys.exit(1)
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{args.gpu}"
    
    test_dataset = MemoryFriendlyLoader(img_dir=str(args.data), task="test")
    test_queue   = torch.utils.data.DataLoader(
        test_dataset,
        batch_size  = 1,
        pin_memory  = True,
        num_workers = 0
    )

    model = Finetunemodel(args.weights)
    model = model.cuda()
    
    # Measure efficiency score
    flops, params, avg_time = mon.calculate_efficiency_score(
        model      = model,
        image_size = args.image_size,
        channels   = 3,
        runs       = 100,
        use_cuda   = True,
        verbose    = False,
    )
    console.log(f"FLOPs  = {flops:.4f}")
    console.log(f"Params = {params:.4f}")
    console.log(f"Time   = {avg_time:.4f}")
    
    #
    model.eval()
    with torch.no_grad():
         sum_time = 0
         with mon.get_progress_bar() as pbar:
            for _, (input, image_name) in pbar.track(
                sequence    = enumerate(test_queue),
                total       = len(test_queue),
                description = f"[bright_yellow] Inferring"
            ):
                input       = Variable(input).cuda()
                start_time  = time.time()
                i, r        = model(input)
                run_time    = time.time() - start_time
                sum_time   += run_time
                image_name  = mon.Path(image_name[0])
                result_path = args.output_dir / image_name.name
                torchvision.utils.save_image(r, str(result_path))
            avg_time = float(sum_time / len(test_queue))
            console.log(f"Average time: {avg_time}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser("SCI")
    parser.add_argument("--data",       type=str, default="./data/medium", help="location of the data corpus")
    parser.add_argument("--weights",    type=str, default="./weights/medium.pt", help="location of the data corpus")
    parser.add_argument("--image-size", type=int, default=512)
    parser.add_argument("--gpu",        type=int, default=0, help="gpu device id")
    parser.add_argument("--seed",       type=int, default=2, help="random seed")
    parser.add_argument("--output-dir", type=str, default="./results/medium", help="location of the data corpus")
    args = parser.parse_args()
    
    args.data       = mon.Path(args.data)
    args.output_dir = mon.Path(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    test(args)
