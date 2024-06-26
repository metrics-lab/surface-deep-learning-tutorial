import os
import sys
import torch

import numpy as np
import nibabel as nb
import pandas as pd

from tools.datasets import dataset_cortical_surfaces, dataset_cortical_surfaces_segmentation

from tools.samplers import new_sampler_HCP_fluid_intelligence,sampler_preterm_birth_age, sampler_preterm_scan_age, sampler_sex_classification, sampler_UKB_scan_age, sampler_HCP_fluid_intelligence, sampler_HCP_scan_age


def loader_metrics(data_path,
                    sampler,
                    config,):

    ###############################################################
    #####################    TRAINING DATA    #####################
    ###############################################################

    train_dataset = dataset_cortical_surfaces(config=config,
                                                data_path=data_path,
                                                split='train',
                                                )

    #####################################
    ###############  dHCP  ##############
    #####################################
    if sampler and config['data']['dataset']=='dHCP' :
        
        if config['data']['task']=='birth_age' :
            print('Sampler: dHCP preterm for birth_age')

            train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}/{}/{}.csv'.format(config['data']['path_to_workdir'],
                                                                                        config['data']['dataset'],
                                                                                        config['data']['task'],
                                                                                        config['data']['hemi'],'train')).labels.to_numpy()
            sampler = sampler_preterm_birth_age(train_labels)
            train_loader = torch.utils.data.DataLoader(train_dataset,
                                                        batch_size = config['training']['bs'],
                                                        sampler=sampler,
                                                        num_workers=32)
        elif config['data']['task']=='scan_age':
            print('Sampler: dHCP preterm for scan_age')

            train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}/{}/{}.csv'.format(config['data']['path_to_workdir'],
                                                                                        config['data']['dataset'],
                                                                                        config['data']['task'],
                                                                                        config['data']['hemi'],'train')).labels.to_numpy()
            sampler = sampler_preterm_scan_age(train_labels)
            train_loader = torch.utils.data.DataLoader(train_dataset,
                                                        batch_size = config['training']['bs'],
                                                        sampler=sampler,
                                                        num_workers=32)
            
        elif config['data']['task']=='sex':
            print('Sampler: dHCP sex classification')

            train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}/{}/{}.csv'.format(config['data']['path_to_workdir'],
                                                                                        config['data']['dataset'],
                                                                                        config['data']['task'],
                                                                                        config['data']['hemi'],'train')).labels.to_numpy()
            sampler = sampler_sex_classification(train_labels)
            train_loader = torch.utils.data.DataLoader(train_dataset,
                                                        batch_size = config['training']['bs'],
                                                        sampler=sampler,
                                                        num_workers=32)
                                            
    #####################################
    ###############  UKB   ##############
    #####################################
    elif sampler and config['data']['dataset']=='UKB':
        
        if config['data']['task']=='sex':
            print('Sampler: UKB sex classification')

            train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}_{}/{}/{}.csv'.format(config['data']['path_to_workdir'],
                                                                                        config['data']['dataset'],
                                                                                        config['data']['task'],
                                                                                        config['data']['registration'],
                                                                                        config['data']['hemi'],'train')).labels.to_numpy()
            sampler = sampler_sex_classification(train_labels)
            train_loader = torch.utils.data.DataLoader(train_dataset,
                                                        batch_size = config['training']['bs'],
                                                        sampler=sampler,
                                                        num_workers=32)

        elif config['data']['task']=='scan_age':
            print('Sampler: UKB scan age regression')

            if config['data']['subset']:
                train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}_{}/{}/{}_sub.csv'.format(config['data']['path_to_workdir'],
                                                                                            config['data']['dataset'],
                                                                                            config['data']['task'],
                                                                                            config['data']['registration'],
                                                                                            config['data']['hemi'],'train')).labels.to_numpy()
            else:
                train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}_{}/{}/{}.csv'.format(config['data']['path_to_workdir'],
                                                                                            config['data']['dataset'],
                                                                                            config['data']['task'],
                                                                                            config['data']['registration'],
                                                                                            config['data']['hemi'],'train')).labels.to_numpy()
            sampler = sampler_UKB_scan_age(train_labels)
            train_loader = torch.utils.data.DataLoader(train_dataset,
                                                        batch_size = config['training']['bs'],
                                                        sampler=sampler,
                                                        num_workers=32)

    #####################################
    ###############  HCP   ##############
    #####################################
    elif config['data']['dataset']=='HCP':
        
        if config['data']['task']=='scan_age':

            print('Sampler: HCP scan_age classification')

            train_labels = pd.read_csv('{}/labels/{}/cortical_metrics/{}/{}/{}.csv'.format(config['data']['path_to_workdir'],
                                                                                        config['data']['dataset'],
                                                                                        config['data']['task'],
                                                                                        config['data']['hemi'],'train')).labels.to_numpy()
            sampler = sampler_HCP_scan_age(train_labels)
            train_loader = torch.utils.data.DataLoader(train_dataset,
                                                    batch_size = config['training']['bs'],
                                                    sampler=sampler,
                                                    num_workers=32,)
    else:
        print('not using sampler...')
        print('shuffling == {}'.format(not config['RECONSTRUCTION']))

        train_loader = torch.utils.data.DataLoader(train_dataset,
                                                        batch_size = config['training']['bs'],
                                                        shuffle=(not config['RECONSTRUCTION']),
                                                        num_workers=32)

    ###############################################################
    ####################    VALIDATION DATA    ####################
    ###############################################################


    val_dataset = dataset_cortical_surfaces(data_path=data_path,
                                                config=config,
                                                split='val',
                                                )
    
    val_loader = torch.utils.data.DataLoader(val_dataset,
                                                batch_size=config['training']['bs_val'],
                                                shuffle=False,
                                                num_workers=32)
                

    ###############################################################
    #####################    TESTING DATA     #####################
    ###############################################################
            

    test_dataset = dataset_cortical_surfaces(data_path=data_path,
                                            config=config,
                                            split='test',
                                            )
    
    test_loader = torch.utils.data.DataLoader(test_dataset,
                                                batch_size=config['training']['bs_val'],
                                                shuffle=False, 
                                                num_workers=32)
    
    train_dataset.logging()
    
    print('')
    print('#'*30)
    print('############ Data ############')
    print('#'*30)
    print('')

    print('')
    print('Training data: {}'.format(len(train_dataset)))
    print('Validation data: {}'.format(len(val_dataset)))
    print('Testing data: {}'.format(len(test_dataset)))

    return train_loader, val_loader, test_loader
    

def loader_metrics_segmentation(data_path,
                                labels_path,
                                sampler,
                                config):

    ###############################################################
    #####################    TRAINING DATA    #####################
    ###############################################################

    train_dataset = dataset_cortical_surfaces_segmentation(config=config,
                                                            data_path=data_path,
                                                            labels_path=labels_path,
                                                            split='train')

    #####################################
    ###############  UKB   ##############
    #####################################


    train_loader = torch.utils.data.DataLoader(train_dataset,
                                                batch_size = config['training']['bs'],
                                                shuffle = True, 
                                                num_workers=32)

    ###############################################################
    ####################    VALIDATION DATA    ####################
    ###############################################################


    val_dataset = dataset_cortical_surfaces_segmentation(data_path=data_path,
                                                config=config,
                                                labels_path=labels_path,
                                                split='val',)

    val_loader = torch.utils.data.DataLoader(val_dataset,
                                            batch_size=config['training']['bs_val'],
                                            shuffle=False,
                                            num_workers=32)
            

    ###############################################################
    #####################    TESTING DATA     #####################
    ###############################################################
            

    test_dataset = dataset_cortical_surfaces_segmentation(data_path=data_path,
                                            config=config,
                                            labels_path=labels_path,
                                            split='test',)


    test_loader = torch.utils.data.DataLoader(test_dataset,
                                            batch_size=config['training']['bs_val'],
                                            shuffle=False, 
                                            num_workers=32)
    
    train_dataset.logging()
    

    print('')
    print('Training data: {}'.format(len(train_dataset)))
    print('Validation data: {}'.format(len(val_dataset)))
    print('Testing data: {}'.format(len(test_dataset)))

    return train_loader, val_loader, test_loader

