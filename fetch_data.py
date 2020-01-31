import os
import numbers
import warnings
from sklearn.utils import Bunch

from nilearn._utils.numpy_conversions import csv_to_array
from nilearn.datasets.utils import (_get_dataset_dir, _fetch_files)


def _fetch_aly_2018_participants(data_dir, url, verbose):
    """Helper function to fetch_aly_2018.
    This function helps in downloading participant data from .tsv file
    uploaded on Open Science Framework (OSF).

    Parameters
    ----------
    data_dir: str
        Path of the data directory. Used to force data storage in a specified
        location. If None is given, data are stored in home directory.
    url: str, optional
        Override download URL. Used for test only (or if you setup a mirror of
        the data). Default: None
    verbose: int
        Defines the level of verbosity of the output.
    Returns
    -------
    participants : numpy.ndarray
        Details each subject's sex and age.
    """
    dataset_name = 'aly_2018'
    data_dir = _get_dataset_dir(dataset_name, data_dir=data_dir,
                                verbose=verbose)

    if url is None:
        url = 'https://osf.io/3gm9p/download/'

    files = [('participants.tsv', url, {'move': 'participants.tsv'})]
    path_to_participants = _fetch_files(data_dir, files, verbose=verbose)[0]

    # Load path to participants
    dtype = [('participant_id', 'U12'), ('sex', 'U4'), ('age', '<f8')]
    names = ['participant_id', 'sex', 'age']
    participants = csv_to_array(path_to_participants, skip_header=True,
                                dtype=dtype, names=names)
    return participants


def _fetch_aly_2018_functional(n_subjects, n_runs, data_dir, url, verbose):
    """Helper function to fetch_aly_2018.
    This function helps in downloading functional MRI data in Nifti
    format and associated regressors for each subject.
    The files are downloaded from Open Science Framework (OSF).
    Parameters
    ----------
    n_subjects : numpy.ndarray
        The number of participants to download. If None, all available
        participants are downloaded. Default: None
    n_runs : int
        The number of runs to download for each participant. If None, all
        available runs are downloaded. Default: None
    data_dir: str
        Path of the data directory. Used to force data storage in a specified
        location. If None is given, data are stored in home directory.
    url: str, optional
        Override download URL. Used for test only (or if you setup a mirror of
        the data). Default: None
    verbose: int
        Defines the level of verbosity of the output.
    Returns
    -------
    func: list of str (Nifti files)
        Paths to functional MRI data (4D) for each subject.
    regressors: list of str (tsv files)
        Paths to regressors related to each subject.
    """
    dataset_name = 'aly_2018'
    data_dir = _get_dataset_dir(dataset_name, data_dir=data_dir,
                                verbose=verbose)

    if url is None:
        url = 'https://osf.io/download/{}/'

    confounds = 'subj-{0}_task-movie_run-{1}_desc-reducedConfounds_regressors.tsv'
    func = ('subj-{0}_task-movie_run-{1}' +
            '_space-MNI152NLin2009cAsym_desc-intactPostproc_bold.nii.gz')

    # The gzip contains unique download keys per Nifti file and confound
    # pre-extracted from OSF. Required for downloading files.
    tutorial_directory = os.path.dirname(os.path.abspath(__file__))
    dtype = [('participant_id', 'U12'), ('run_num', 'U12'),
             ('key_r', 'U24'), ('key_b', 'U24')]
    names = ['participant_id', 'run_num', 'key_r', 'key_b']
    # csv file contains download information related to OSF
    osf_data = csv_to_array(os.path.join(tutorial_directory, "aly_2018.csv"),
                            skip_header=True, dtype=dtype, names=names)

    funcs = []
    regressors = []

    if n_subjects is None:
        n_subjects = 30

    for subj in range(1, n_subjects + 1):
        subj_files = osf_data[osf_data['participant_id'] == str(subj).zfill(2)]
        if n_runs is not None:
            subj_files = subj_files[:n_runs]

        for f in subj_files:
            # Download regressors
            confound_url = url.format(f['key_r'])
            regressor_file = [(confounds.format(f['participant_id'], f['run_num']),
                               confound_url,
                               {'move': confounds.format(f['participant_id'],
                                                         f['run_num'])}
                               )]
            path_to_regressor = _fetch_files(data_dir, regressor_file,
                                             verbose=verbose)
            regressors.append(path_to_regressor)

            # Download bold images
            func_url = url.format(f['key_b'])
            func_file = [(func.format(f['participant_id'], f['run_num']), func_url,
                          {'move': func.format(f['participant_id'], f['run_num'])}
                          )]
            path_to_func = _fetch_files(data_dir, func_file, verbose=verbose)[0]
            funcs.append(path_to_func)
    return funcs, regressors


def fetch_aly_2018(n_subjects=None, n_runs=None,
                   data_dir=None, resume=True, verbose=1):
    """Fetch fMRI dataset targeting the medial temporal lobe (MTL)
    during repeated movie-watching. Created by Aly and colleagues
    and originally downloaded from OpenNeuro. See Notes below.

    Parameters
    ----------
    n_subjects: int, optional (default None)
        The number of subjects to load. If None, all the subjects are
        loaded. Maximum of 30 subjects.
    n_runs: int, optional (default None)
        The number of runs to load per subject. If None, all the runs are
        loaded. Maximum of 2 runs.
    data_dir: str, optional (default None)
        Path of the data directory. Used to force data storage in a specified
        location. If None, data are stored in home directory.
    resume: bool, optional (default True)
        Whether to resume download of a partly-downloaded file.
    verbose: int, optional (default 1)
        Defines the level of verbosity of the output.

    Returns
    -------
    data: Bunch
        Dictionary-like object, the interest attributes are :
        - 'func': list of str (Nifti files)
            Paths to downsampled functional MRI data (4D) for each subject.
        - 'confounds': list of str (tsv files)
            Paths to confounds related to each subject.
        - 'phenotypic': numpy.ndarray
            Details each subject's sex and age.

    Notes
    -----
    The original data is downloaded from OpenNeuro
    https://openneuro.org/datasets/ds001545/versions/1.0.0

    This fetcher downloads downsampled data that are available on Open
    Science Framework (OSF). Located here: https://osf.io/vgj7w/files/
    Preprocessing details: https://osf.io/479pt/

    References
    ----------
    Please cite this paper if you are using this dataset:
    Aly M, Chen J, Turk-Browne NB, & Hasson U (2018).
    Learning naturalistic temporal structure in the posterior medial network.
    Journal of Cognitive Neuroscience, 30(9): 1345-1365.
    https://www.mitpressjournals.org/doi/full/10.1162/jocn_a_01308
    """

    dataset_name = 'aly_2018'
    data_dir = _get_dataset_dir(dataset_name, data_dir=data_dir,
                                verbose=verbose)

    # Participants data: ids, demographics, etc
    participants = _fetch_aly_2018_participants(data_dir=data_dir,
                                                url=None,
                                                verbose=verbose)

    max_subjects = len(participants)
    if n_subjects is None:
        n_subjects = max_subjects

    if (isinstance(n_subjects, numbers.Number) and
            ((n_subjects > max_subjects) or (n_subjects < 1))):
        warnings.warn("Wrong value for n_subjects={0}. The maximum "
                      "value will be used instead n_subjects={1}"
                      .format(n_subjects, max_subjects))
        n_subjects = max_subjects

    if (isinstance(n_runs, numbers.Number) and
       ((n_runs > 2) or (n_runs < 1))):
        warnings.warn("Wrong value for n_runs={0}. The maximum "
                      "value will be used instead n_runs={1}"
                      .format(n_subjects, 2))
        n_runs = 2

    funcs, regressors = _fetch_aly_2018_functional(n_subjects=n_subjects,
                                                   n_runs=n_runs,
                                                   data_dir=data_dir,
                                                   url=None,
                                                   verbose=verbose)

    return Bunch(func=funcs, confounds=regressors, phenotypic=participants)
