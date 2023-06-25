import numpy as np
from rsatoolbox import rdm, vis
from utils import time_series
from build_connectome import connectivity_matrix


def rsa(subjects_df, conf_strategy, atlas, low_pass, high_pass, smoothing_fwhm, t_r, output):
    behavioral_distance_matrix = behavioral_distance(subjects_df)

    timeseries = subjects_df.apply(lambda subj: time_series(subj['func_path'], subj['mask_path'],
                                                            conf_strategy, atlas.maps,
                                                            low_pass, high_pass, smoothing_fwhm,
                                                            t_r), axis=1)
    connectivity_matrices = np.stack(timeseries.apply(lambda ts: connectivity_matrix([ts])[0][0]))
    connectivity_distance_matrix = connectivity_distance(connectivity_matrices)

    rdm_connectivity = get_rdm(connectivity_distance_matrix[None, :],
                               descriptor=f'Connectivity_{atlas.name}',
                               pattern_descriptors=subjects_df.index.to_list())
    rdm_behavior = get_rdm(behavioral_distance_matrix[None, :],
                           descriptor='Behavioral',
                           pattern_descriptors=subjects_df.index.to_list())

    fig_connectivity = vis.scatter_plot.show_2d(rdm_connectivity,
                                                method='MDS',
                                                rdm_descriptor='name',
                                                pattern_descriptor='subjects')

    fig_behavior = vis.scatter_plot.show_2d(rdm_behavior,
                                            method='MDS',
                                            rdm_descriptor='name',
                                            pattern_descriptor='subjects')

    output.mkdir(exist_ok=True, parents=True)
    fig_connectivity.savefig(output / f'connectivity_{atlas.name}.png')
    fig_behavior.savefig(output / 'behavior.png')

    return rdm_behavior, rdm_connectivity


def behavioral_distance(subjects_df):
    fields = ['edad', 'composite_attention', 'composite_visuoespatial', 'composite_language', 'composite_memory',
              'composite_executive']
    behavioral_data = subjects_df[fields]
    behavioral_data /= behavioral_data.std()
    behavioral_distance = np.linalg.norm(behavioral_data.values[:, None] - behavioral_data.values[None, :], axis=2)

    return behavioral_distance


def connectivity_distance(connectivity_matrices):
    connectivity_std = np.std(connectivity_matrices, axis=0)
    np.fill_diagonal(connectivity_std, 1)
    # Compute the distance between correlation matrices
    n_subjects = connectivity_matrices.shape[0]
    connectivity_distance_matrix = np.empty((n_subjects, n_subjects))
    for i in range(n_subjects):
        for j in range(n_subjects):
            connectivity_distance_matrix[i, j] = np.linalg.norm((connectivity_matrices[i, :] -
                                                                 connectivity_matrices[j, :]) / connectivity_std)

    return connectivity_distance_matrix


def get_rdm(distance_matrix, descriptor, pattern_descriptors):
    rdm_obj = rdm.RDMs(distance_matrix,
                       dissimilarity_measure='Euclidean',
                       rdm_descriptors={'name': [descriptor]},
                       pattern_descriptors={'subjects': pattern_descriptors})
    rdm_obj = rdm.transform(rdm_obj, lambda x: x / x.max())

    return rdm_obj
