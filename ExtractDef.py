from requests import get
from bs4 import BeautifulSoup
from re import findall
from googlesearch import search
from pandas import DataFrame

def ExtractText(url:str) -> str:
    TempStringDataInfo = ""
    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        TempStringDataInfo = soup.get_text()
    return TempStringDataInfo

def ExtractNumberFromText(text:str, numberLen:int = 10) -> list:
    return [s for s in findall(r'-?\d+\.?\d*', text) if len(s) == numberLen]

def AppExtract(Search, num_results: int = 10, lang: str = "en") -> dict:
    DataFrameExcel = {}
    resultSearch = search(Search, num_results=num_results, lang=lang)
    for iterUrls in resultSearch:
        text = ExtractText(iterUrls)
        result = ExtractNumberFromText(text)
        DataFrameExcel[iterUrls] = result
    return DataFrameExcel

def ConvertToExcel(name:str, DictConvertToExcel:dict):
    resultDataFrame = DataFrame.from_dict(DictConvertToExcel, orient="index")
    temporal = resultDataFrame.transpose()
    temporal.to_excel(f"{name}.xlsx")