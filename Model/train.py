# from utils import *
from fastai.vision.core import *
from fastai.vision.data import *
from fastbook import *
import os

DATA_PATH = '../data/full/'
OUT_PATH = '../data/outputs/'
os.listdir(DATA_PATH)

# Create DataBlock instance
data = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(512))

# Load data
dls = data.dataloaders(DATA_PATH)

# Display pictures and labels
dls.valid.show_batch(max_n=10, nrows=2)