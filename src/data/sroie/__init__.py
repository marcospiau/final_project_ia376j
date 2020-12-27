from typing import List, Dict
import glob
import json
import os
from torch.utils.data import Dataset, DataLoader

SROIE_FIELDS_TO_EXTRACT = ['address', 'date', 'total', 'company']


def load_labels(key_path: str) -> dict:
    """Loads labels, filling missing values with empty string.

    """
    required_keys = ['company', 'date', 'address', 'total']
    defaults = dict((k, '') for k in required_keys)

    text_data = json.load(open(f'{key_path}.txt', 'r'))
    # text_data = defaultdict(lambda: '', text_data)
    text_data = {**defaults, **text_data}
    return text_data


def load_full_ocr(key_path: str) -> dict:
    """Loads full output from Google Vision OCR.

    """
    text_data = json.load(open(f'{key_path}.json', 'r'))
    return text_data


def get_all_keynames_from_dir(base_dir: str) -> List[str]:
    """Gets all keynames (filenames without extensions) from dir.

    """
    # all_files = os.listdir(base_dir)
    all_files = glob.glob(base_dir + '/*')
    keynames = sorted(set([os.path.splitext(x)[0] for x in all_files]))
    return keynames


def get_dataloaders_dict_from_datasets_dict(
        datasets_dict: Dict[str, Dataset],
        dataloader_kwargs: dict) -> Dict[str, DataLoader]:
    """Generates dataloaders dict from datasets dict.

    Args:
        datasets_dict (Dict[str, Dataset]): dict of dataxets
        dataloader_kwargs (dict): kwargs for dataloader initialization.

    Returns:
        Dict[str, DataLoader]: dict with dataloaders.
    """
    dataloaders = {
        k: DataLoader(v, **dataloader_kwargs)
        for k, v in datasets_dict.items()
    }
    return dataloaders