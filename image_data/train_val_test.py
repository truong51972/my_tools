import glob
from pathlib import Path
import random
import shutil

def split(
    src : str,
    des : str,
    train : float = 0.7,
    val : float = 0.2,
    test : float = 0.1,
    percent_of_data : float = 1,
    shuffle = True,
):
    '''
        Split image data from `src` to `des` with `percent_of_data`.

        Args:
            src (str): source of image data.
            des (str): destination of image data.
            train (float): percent of train data.
            val (float): percent of val data.
            test (float): percent of test data.
            percent_of_data (float): percent of number of images compare with raw data.
            shuffle (bool): shuffle data before splitting.

        Returns:
            None

    '''
    
    src = Path(src)
    des = Path(des)

    if percent_of_data > 1 : raise "Percent of data must be less or equal 1!"
    if sum(train, val, test) != 1 : raise "Total of train, val, test must be 1!"

    class_paths = glob.glob(str(src / '*'))

    for class_path in (class_paths):
        class_name = class_path.split('\\')[-1]
        img_paths = glob.glob(class_path + '/*')

        if shuffle: random.shuffle(img_paths)

        nums_of_imgs = int(len(img_paths)* percent_of_data)
        for i in range(nums_of_imgs):
            img_path = img_paths[i]
            img_name = img_path.split('\\')[-1]

            if i <= int(nums_of_imgs * train):
                tar = "train"
            elif i <= int(nums_of_imgs * (train+val)):
                tar = "val"
            else:
                tar = "test"

            des_class = des / tar / class_name 
            des_class.mkdir(parents=True, exist_ok=True)
    
            shutil.copy(img_path, des_class / img_name)

    print("Done!")
    
if __name__ == "__main__":
    pass