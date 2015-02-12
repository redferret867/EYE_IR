import random
from random import choice
from random import shuffle
import string
import os
from glob import glob
from copy import deepcopy

# for troubleshooting, will be deleted
test_block_len = 40
study_block_len = 20
num_blocks = 12

# stim pool
#sound_file_pool = glob('*.wav')

# for testing without sound files
sound_file_pool = []
for s in range(0,499):
    sound_file_pool.append(s)

# for troubleshooting    
#print sound_file_pool[0:10]
    
# shuffle them
random.shuffle(sound_file_pool)

def gen_test_block(sound_file_pool,test_block_len,target_items):

    # make a list for test_block and lure_items
    test_block = []
    lure_items = []
    
    # reset the count so I can reuse this var
    count = 0
    
    # put the remaining items from sound_file_pool into a list of lure items
    for l in range(test_block_len/2):
        lure_items.append(sound_file_pool.pop())
        
    # create test_blocks with targets from the study_blocks and lures
    for t in range(test_block_len):
        
        # more shuffling
        random.shuffle(lure_items)
        random.shuffle(target_items)
    
        # fill half of the test_block with targets
        if len(test_block) < (test_block_len/2):
            
            # gives a unique index number
            count += 1
            
            # creates a dictionary for each study_trial with the given keys
            test_trial = {'index':count,
                        'block_type':'test',
                        'trial_type':'target',
                        'isi':random.randint(1000.0,2000.0)/1000.0,
                        'resp_time':0.0,}

            # set the sound from the sound_files list // I don't understand this bit
            test_trial['stim']=target_items.pop()
        
            # shuffle and append the target item to the test_block
            random.shuffle(test_block)
            test_block.append(test_trial)
        
        # fill the second half of the test_block with lures
        elif (len(test_block) > (test_block_len/2)) and (len(test_block) < (test_block_len)):
        
            # gives a unique index number
            count += 1
        
            # creates a dictionary for each study_trial with the given keys
            test_trial = {'index':count,
                        'block_type':'test',
                        'trial_type':'lure',
                        'isi':random.randint(1000.0,2000.0)/1000.0,
                        'resp_time':0.0,}

            # adds the lure to the trial dictionary with the key 'stim'
            test_trial['stim']=lure_items.pop()
            
            # shuffle and append the lure item to the test_block
            random.shuffle(test_block)
            test_block.append(test_trial)
            
    return test_block

def gen_block(sound_file_pool,study_block_len,test_block_len):

    """
    Generate a list of placeholders. Each placeholder is a 
    dictionary with the following keys:
        index       Index into the item list
        block_type  Study or test
        trial_type  Target or lure
        isi         Variable interstimulus interval
        resp_time   Time until subject response
    """

    # prepare to fill study block with dictionaries that are each trial
    study_block = []
    
    # target items to feed to gen_test_block to make target blocks
    target_items = []
    
    # grabs a sound file from sound_file_pool and puts one copy in the study block
    # puts a second copy with only the 'stim' key in the target_items list to make test_blocks
    # I am unsure that the current iteration of this for-loop and the gen_test_block function
    # will correctly associate the targets in a test_block with the correct study_block
    for c in range(study_block_len):
        # shuffle the sound files
        random.shuffle(sound_file_pool)

        # creates a dictionary for each study_trial with the given keys
        study_trial = {'index':0,
                        'block_type':'study',
                        'trial_type':'target',
                        'isi':random.randint(1000.0,2000.0)/1000.0,
                        'resp_time':0.0,}

        # adds the sound to the trial dictionary with the key 'stim'
        study_trial['stim']=sound_file_pool.pop()

        # shuffling
        shuffle(study_block)
        
        # add this trial to the study block
        study_block.append(study_trial)
        
        # store the sound file to use as a target in test_block
        target_items.append(study_trial['stim'])
  
    for n,i in enumerate(study_block):
        i['index']= n + 1

    # generate test_blocks for the test portion of the experiment
    test_block = gen_test_block(sound_file_pool,test_block_len,target_items)
    
    # for readable troubleshooting
    for trial in study_block:
        print trial
    print '\n'
    for trial in test_block:
        print trial
    
    return study_block,test_block
gen_block(sound_file_pool,study_block_len,test_block_len)
    
def gen_blocks(sound_file_pool,study_block_len,test_block_len,num_blocks):
    
    # make empty list to hold all study blocks
    sb = []
    
    # empty list to hold test blocks
    tb = []
    
    # make each study block and update
    for b in range(num_blocks):
        
        study,test = gen_block(sound_file_pool,study_block_len,test_block_len)

        # add block to list of study or test blocks
        sb.append(study)     
        tb.append(test)
    
    #print sb
    #print tb
    
    return sb,tb
#gen_blocks(sound_file_pool,study_block_len,test_block_len,num_blocks)