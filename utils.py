import pandas as pd
import numpy as np
from nilearn import datasets


def load_atlas(atlas_name):
    if atlas_name == 'aal':
        atlas = datasets.fetch_atlas_aal()
        atlas.labels = pd.DataFrame({'name': atlas.labels})
    elif atlas_name == 'destrieux':
        atlas = datasets.fetch_atlas_destrieux_2009(legacy_format=False)
        # Remove missing regions in atlas.maps from atlas.labels
        # (0 == 'background', 42 == 'L Medial_wall', 117 == 'R Medial_wall)
        atlas.labels = atlas.labels.drop([0, 42, 117]).reset_index(drop=True)
    elif atlas_name == 'schaefer':
        atlas = datasets.fetch_atlas_schaefer_2018(n_rois=100)
        # Remove '7Networks_' prefix
        atlas.labels = pd.DataFrame({'name': [label[10:].decode() for label in atlas.labels]})
    else:
        raise ValueError(f'Atlas {atlas_name} not recognized')

    return atlas


def load_clinical_data(clinical_datafile):
    cg = pd.read_csv(clinical_datafile)
    subjects_data = cg[~cg['AnonID'].isna()]
    subjects_data = subjects_data.astype({'AnonID': int})
    subjects_data = subjects_data.set_index('AnonID')

    # Remove invalid subjects (subj 29 has different data shapes)
    subjects_to_remove = [2, 17, 29]
    subjects_data = subjects_data.drop(subjects_to_remove)
    # Remove subjects with no cluster
    subjects_data = subjects_data[~subjects_data['cluster'].isna()]

    return subjects_data


def load_datapaths(subjects_paths, subjects_df):
    for subj_path in subjects_paths:
        subj_id = int(subj_path.name.split('-')[1])
        if subj_id in subjects_df.index:
            # Get the path to the preprocessed functional data
            func_path = subj_path / 'func'
            func_file = [f for f in func_path.glob('*.nii.gz') if 'preproc' in f.name][0]
            mask_file = [f for f in func_path.glob('*.nii.gz') if 'brain_mask' in f.name][0]
            subjects_df.loc[subj_id, 'func_path'] = str(func_file)
            subjects_df.loc[subj_id, 'mask_path'] = str(mask_file)


def apply_threshold(connectivity_matrix, threshold):
    percentile = np.percentile(connectivity_matrix, threshold)
    connectivity_matrix[connectivity_matrix < percentile] = 0
    return connectivity_matrix


def q_test(data, mean):
    # Upper triangulate the data
    data, mean = np.triu(data, k=1), np.triu(mean, k=1)
    q = np.sum(np.sum(np.square(data - mean)) / (len(data) - 1))
    return q