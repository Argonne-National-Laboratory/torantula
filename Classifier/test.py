import sys
import DataSet
from DataSet import get_file_cat
import sklearn
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    '''
    This file exists to test the basic functionality of the dataset class and serves
    to show how we might begin training and testing classifiers on future datasets.
    '''

    #initialize a DataSet object to our data directory
    data = DataSet.DataSet(sys.argv[1])
    print 'dataset loaded'

    #build a list containing proper label for each input file
    labels = []
    for x in data.get_flat_files():
        labels.append(data.get_tag(get_file_cat(x)))

    print "files: "
    print data.get_flat_files()

    print "categories: "
    print data.get_categories()

    print '\n'
    print 'BEGIN MACHINE LEARNING'

    #instanciate count vectorizer and perform feature extraction on input text
    count_vect = CountVectorizer(input=u'filename')
    features = count_vect.fit_transform(data.get_flat_files())

    #randomly split data and labels into training and testing datasets
    features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels, test_size=0.2, random_state=14)

    print "len training set: " + str(len(labels_train))
    print "len test set: " + str(len(labels_test))

    print '\n'

    #initialize, fit, and predict a multinomialNB classifier on our data
    print "MultinomialNB"
    clf = MultinomialNB()
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    acc = accuracy_score(labels_test, pred)

    #perform cross validation testing on randomized folds of data
    print "CROSS VALIDATION"
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(clf, features, labels, cv=5)
    print "cross val scores: "
    print scores

    print "accuracy: " + str(acc)


if __name__ == "__main__":
    main()
