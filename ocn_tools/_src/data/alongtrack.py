import pandas as pd
import copernicusmarine
from tqdm.auto import tqdm


ALONGTRACK_NAMES = [
    "c2",
    "h2",
    "al",
    "j3",
    "s3",
    "s6",
    "swon"
]


def download_alongtrack_data(
        satellite: str = "c2",
        time_min: str = "2017-01-01",
        time_max: str = "2017-02-01",
        output_directory: str = ".",
        **kwargs
):  
    # get dataset ID
    dataset_id = f'cmems_obs-sl_glo_phy-ssh_nrt_{satellite}-l3-duacs_PT1S'
    # filter for time periods
    filters = filter_alongtrack_times(time_min=time_min, time_max=time_max)

    print(dataset_id, filters)

    for filt in filters:
        copernicusmarine.get(
            dataset_id=dataset_id,
            filter=filt,
            output_directory=output_directory,
            force_download=True,
            overwrite_output_data=True,
            **kwargs
        )


def filter_alongtrack_times(time_min, time_max):
    return set([f"*{d.year}{d.month:02}*" for d in pd.date_range(time_min, time_max)])
