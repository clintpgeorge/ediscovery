import numpy as np
import pyradbas.pyradbas as pyrb

#import matplotlib.pyplot as plt
##Defines the mesh
#x = np.linspace(-1.5, 1.5, 40)
#x, y = np.meshgrid(x, x)
#P = np.vstack([x.flatten(), y.flatten()])
#
##Defines the function
#heart = lambda x,y: np.abs(x**2.+2*(y-0.5*np.sqrt(np.abs(x)))**2.-1)
#
##Evaluates function over every point of the grid
#V = heart(P[0:1], P[1:])
#
##Plot
#plt.plot(P[0:1][V<0.2], P[1:][V<0.2], '*r', P[0:1][V>=0.2], P[1:][V>=0.2], 'o')
#plt.show()
#
##defines an exact RBFN
#enet = pyrb.train_exact(P.T, V.T, 0.3)
#
##simulate
#S = enet.sim(P.T).T
#plt.plot(P[0:1][S<0.2], P[1:][S<0.2], '*r', P[0:1][S>=0.2], P[1:][S>=0.2], 'o')
#plt.show() # small differences are due to ill conditioning
#
##What if we compute points outside training set
#O=np.random.uniform(size=(2,5000), low=-2., high=2.)
#S = enet.sim(O.T).T
#plt.plot(O[0:1][S<0.2], O[1:][S<0.2], '*r', O[0:1][S>=0.2], O[1:][S>=0.2], 'o')
#plt.show()


import os 
from utils.utils_file import read_config, load_file_paths_index

RELEVANT_CLASS_ID = 0
IRRELEVANT_CLASS_ID = 1

def get_rbf_classification_dataset(mdl_cfg_file, positive_dir):   
    
    mdl_cfg = read_config(mdl_cfg_file)

    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file)    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.float)
    num_docs, num_topics = lda_theta.shape
    
    print 'LDA Theta: Number of documents ', num_docs, ' number of topics ', num_topics  
    
    class_ids = []
    file_paths = [] 
    for (_, root, file_name) in lda_file_path_index:
        if os.path.exists(os.path.join(positive_dir, file_name)):
            class_ids.append(RELEVANT_CLASS_ID)
        else:
            class_ids.append(IRRELEVANT_CLASS_ID)
        file_paths.append(os.path.normpath(os.path.join(root, file_name)))
        
    return (np.array(class_ids), lda_theta, file_paths)


def plot_tm_rbf_decision_values(class_ids, dec_values, dec_values_file=''):
    
    import pylab as pl
    from collections import defaultdict
    
    print 
    true_class = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        print '#%d true class: %d decision value: %.5f' % (i, class_id, dec_values[i])
        true_class[class_id] += [dec_values[i]]
    print 
    
    pl.plot(true_class[IRRELEVANT_CLASS_ID], 'bo', label='Irrelevant')
    x2 = range(len(true_class[IRRELEVANT_CLASS_ID]), len(class_ids))
    pl.plot(x2, true_class[RELEVANT_CLASS_ID], 'r+', label='Relevant')
    pl.axhline(0, color='black')
    pl.xlabel('Documents')
    pl.ylabel('Decision values (c-SVM)')
    pl.title('SVM decision values Query #%d' % query_id)
    pl.legend(loc='lower right', prop={'size':9})
    pl.grid(True)

    if (dec_values_file == ''):
        pl.show()
    else: 
        pl.savefig(dec_values_file, dpi=300, bbox_inches='tight', pad_inches=0.1)


if __name__ == '__main__':
    
    
    query_id = 201
    mdl_cfg_file = "project-%d.cfg" % query_id # configuration file 
    test_directory = "F:\\Research\\datasets\\trec2010\\%d" %  query_id # the directory where we keep the training set (TRUE negatives and TRUE positives) 
    positive_dir = os.path.normpath(os.path.join(test_directory, "1")) # TRUE positive documents 
    dec_values_file = mdl_cfg_file.replace('.cfg', '-rbf-dec.png') 
    
    
    # Loads the RBF dataset from the given topic model 
    class_ids, lda_theta, file_paths = get_rbf_classification_dataset(mdl_cfg_file, positive_dir)
    
    
    # defines an exact RBFN
    enet = pyrb.train_exact(lda_theta, class_ids, 0.05)
    
    # simulate
    dec_values = enet.sim(lda_theta)
    
    plot_tm_rbf_decision_values(class_ids, dec_values, dec_values_file)


