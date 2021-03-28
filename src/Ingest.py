import pandas as pd
import logging


def ingest(path: str, file: str) -> pd.DataFrame:
    logging.debug("Entering ingest()...")
    file_extension = file[-5:]
    full_name = path + file
    if file_extension == ".xlsx":
        data = readExcel(full_name)
    else:
        logging.warning(f"File type '{file_extension}' is not supported.")
        raise TypeError
    logging.debug("Exiting ingest()...")
    return data


def readExcel(filename: str) -> pd.DataFrame:
    logging.debug("Entering readExcel()...")
    try:
        data = pd.read_excel(io=filename, header=0, engine='openpyxl', na_filter=False, sheet_name=None)
        keys = data.keys()
        for key in keys:
            df1 = data[key]
        logging.debug("Exiting readExcel()...")
        return df1
    except FileNotFoundError as e:
        logging.error(e)
        exit(1)

