import glob
import os

class DataSet:
    """
    This class is designed to load a list of filenames and assign labels to a
    pre-categorized training data directory. If structured correctly a data set
    of a variable number of categories will automatically be loaded and category
    names will be extracted from the file path of each file.
    """

    def __init__(self, data_dir):
        """
        An instance of a Dataset object has three elements. when initilized we
        first assign a list of the category subdirectories to 'dirs'. Next we
        initialize each of it's three elements.

        This class should be intialized with the topmost directory of a Dataset
        organized per the 'readme'

        'filenames': create a list of all data files in each of these directories

        'categories': extracted from the filenames of the category directories.

        'tag_dict': assigns and maps each category to it's numerical label
        """

        dirs = [str(data_dir + '/' + x + '/') for x in os.listdir(data_dir)]
        self.filenames = [glob.glob(str(x + '/*.txt')) for x in dirs]
        self.categories = [x.split('-')[0] for x in os.listdir(data_dir)]
        self.tag_dict = {y:x for x,y in dict(enumerate(self.categories)).iteritems()}

    #return full list of filenames. Returns list of lists
    def get_filenames(self):
        return self.filenames

    #return flat file list of all files
    def get_flat_files(self):
        flat_files = [x for y in self.filenames for x in y]
        return flat_files

    #get the label number for a category name
    def get_tag(self, string):
        return self.tag_dict.get(string)

    #return full list of categories
    def get_categories(self):
        return self.categories

    #return tag dictionary
    def get_tag_dict(self):
        return self.tag_dict

#for use with files from filenames list. Returns category name.
def get_file_cat(filename):
    return filename.split('/')[-2].split('-')[0]
