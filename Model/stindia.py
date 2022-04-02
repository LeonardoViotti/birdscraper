from utils import *
# from fastai.vision.core import *
# from fastai.vision.data import *
import os

DATA_PATH = '/notebooks/storage/startup-india/'
OUT_PATH = '/notebooks/outputs/'
# os.listdir(DATA_PATH)

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

# Resize images to 224 pixels
data = data.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms=aug_transforms())
dls = data.dataloaders(DATA_PATH)
# Display pictures and labels
dls.valid.show_batch(max_n=10, nrows=2)

# Create learner with resnet 18 layers 
learn = cnn_learner(dls, resnet18, metrics=error_rate)

# Train for 4 epochs
learn.fine_tune(4)

# Check confusion matrix
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(5, nrows=5)

# Export model
learn.export(OUT_PATH + 'gmodel.pkl')

# import model
learn_inf = load_learner(OUT_PATH + 'gmodel.pkl')

learn_inf.predict('/notebooks/storage/eu.jpg' )