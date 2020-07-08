import json
import glob, os
import sys
import time
import matplotlib.pyplot as plt
from random import seed
from random import randint

# Use skimage for data manipulation
import skimage
from skimage import io
from skimage.transform import resize

"""
    Goal  : Downsample images that we are going to train the GAN on. Since we're
            downsampling
    TODO  : - Downsample command for somethign other than a folder, maybe simply
            an array already preloaded?
            -
    IDEAS : it might be worthwhile to train a GAN to recreate
            real images from pixelated ones. (e.g.
     https://towardsdatascience.com/the-end-to-all-blurry-pictures-f27e49f23588)
"""

def downsample_dir(img_dir, img_size=(64,64), SHOW=False):
    """
    Input :
        img_dir : path to directory with all subfolders and images
        img_size : new (height,width) in pixels
    """

    img_ds_dir = img_dir + "_DS"

    # Create a directory that is Images_DS (downsampled)
    if not os.path.exists(img_ds_dir):
        os.makedirs(img_ds_dir)

    # for visualizing an image
    show_img = randint(0,200); i = 0;

    print("\n--downsampling images--" + ':\n')
    print("Progress" + ':\n')
    nbr_files = sum([len(files) for r, d, files in os.walk(img_dir)])
    i = 1
    for path, subdirs, files in os.walk(img_dir):
        for filename in files:
            # Progress bar
            sys.stdout.write("\r" + str(i) + '/' + str(nbr_files))
            sys.stdout.flush()

            # have only relative paths to images
            rel_dir = os.path.relpath(path, img_dir)
            # create subdir in _DS
            if not os.path.exists(img_ds_dir + os.sep + rel_dir):
                os.makedirs(img_ds_dir + os.sep + rel_dir)
            rel_file = os.path.join(rel_dir, filename)
            img = io.imread(img_dir + os.sep + rel_file)
            # converting to uint8 for no lossy conversion. Might want to change
            # back to float 64
            img_resized = skimage.img_as_ubyte( resize(img, img_size,
                                                       anti_aliasing=True))
            # visualize one of the images
            if i==show_img and SHOW:
                fig, axes = plt.subplots(nrows=1, ncols=2)

                ax = axes.ravel()

                ax[0].imshow(img); ax[0].set_title("Original image")

                ax[1].imshow(img_resized);
                ax[1].set_title("Rescaled image (aliasing)")
                plt.tight_layout(); plt.show()
            io.imsave(img_ds_dir + os.sep + rel_file, img_resized)
            i+=1
    return 0

if __name__ == '__main__':
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    img_dir = curr_dir + os.sep + "Images"

    downsample_dir(img_dir,SHOW=True)

################ OLD CODE #############################
"""
class CustomDataSet(Dataset):
    # Make our own dataset, without labels
    def __init__(self, main_dir, transform):
        self.main_dir = main_dir
        self.transform = transform
        all_imgs = os.listdir(main_dir)
        self.total_imgs = natsort.natsorted(all_imgs)

    def __len__(self):
        return len(self.total_imgs)

    def __getitem__(self, idx):
        img_loc = os.path.join(self.main_dir, self.total_imgs[idx])
        image = Image.open(img_loc).convert("RGB")
        tensor_image = self.transform(image)
        return tensor_image

def scikit_downsample( img_dir, img_size = (64,64), save_img=False ):
    # image_size = (height, width)

    img = io.imread( img_dir + os.sep + "1.jpg" )

    img_original = img

    img_resized = resize(img, img_size, anti_aliasing=True) #False

    if save_img:


    return img, img_resized

def pytorch_downsample( img_dir, img_size = (64,64) , label = None):
    # image_size = (height, width)

    trsfm = transforms.Compose([transforms.Resize( img_size )])
    if label==None:
        dset_original = dset.ImageFolder(root= img_dir+ os.sep)
        dset_resized = dset.ImageFolder(root= img_dir+ os.sep, transform=trsfm)
    else:
        dset_original = CustomDataSet(root= img_dir+ os.sep)
        dset_resized = CustomDataSet(img_dir + os.sep + label, transform=trsfm)

    return dset_original, dset_resized

    if __name__ == '__main__':
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        img_dir = curr_dir + os.sep + "Images"
        human_dir = img_dir + os.sep + "Human"
        label = "Human"

        dset_og, dset_ds = pytorch_downsample(img_dir,label)

        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                             shuffle=True, num_workers=workers)

        fig, axes = plt.subplots(nrows=1, ncols=2)

        ax = axes.ravel()

        #ax[0].imshow(img_og, cmap='gray')
        img_nbr = 0
        ax[0].imshow(img_og[img_nbr])
        ax[0].set_title("Original image")

        ax[1].imshow(img_og[img_nbr])
        ax[1].set_title("Downsampled image")

        plt.tight_layout()
        plt.show()

"""
