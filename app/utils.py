from fastapi import UploadFile

async def read_and_deduplicate_csv(file: UploadFile):
    # Read file contents and split into list
    contents = await file.read()
    start_urls = contents.decode("utf-8").strip().split("\n")

    # Remove duplicates
    start_urls = list(set(start_urls))

    return start_urls
