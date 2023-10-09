from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from scrapy.crawler import CrawlerRunner
from starlette.staticfiles import StaticFiles
import jinja_partials

from app.db import disconnect_from_db, setup_db, connect_to_db, database, insert_new_url, \
    get_all_url_data, reset_all_url_data
from app.spiders import KeywordSearchSpider
from app.utils import read_and_deduplicate_csv

app = FastAPI(debug=True)
runner = CrawlerRunner()

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/templates")

jinja_partials.register_starlette_extensions(templates)


@app.on_event("startup")
async def startup():
    setup_db()
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    rows = await get_all_url_data()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rows": rows,
        }
    )


@app.post("/upload_new_file", response_class=HTMLResponse)
async def upload_new_file(request: Request, file: UploadFile = File(...)):

    # If file is not .csv
    if file.content_type != "text/csv":

        # Return error message and do not swap
        return templates.TemplateResponse(
            "partials/_table_results.html",
            context={"request": request, "error": "File must be a .csv"},
            headers={"HX-Reswap": "none"})

    # Read file contents and remove duplicates
    start_urls = await read_and_deduplicate_csv(file)

    # Clear database
    await reset_all_url_data()

    # Insert each url into database
    async with database.transaction():
        for new_url in start_urls:
            await insert_new_url(new_url)

    # Fetch all (updated) rows from database
    rows = await get_all_url_data()

    return templates.TemplateResponse(
        "partials/_table_results.html",
        {"request": request, "rows": rows},
    )


@app.post("/start_crawler")
async def start(keywords: str = Form(...), start_urls: str = Form(...)):
    runner.crawl(KeywordSearchSpider, start_urls=start_urls, keywords=keywords)
    return {"status": "crawler started"}


@app.post("/stop")
async def stop():
    runner.stop()
    return {"status": "crawler stopped"}
