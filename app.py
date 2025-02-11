from os import getcwd

from fastapi import FastAPI, UploadFile, File
from starlette.middleware.cors import CORSMiddleware

from utils.mongo_util import create_db, add_data, get_drugs_by_defect, client
from utils.predict import predict

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PATH_FILES = getcwd() + "/"

# add background process
@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    # save image as image.jpg
    image_path = "image.jpg"
    with open(image_path, "wb") as buffer:
        buffer.write(file.file.read())

    prediction, prediction_percentage = predict(image_path)
    print(prediction, prediction_percentage)

    defect_collection, drug_collection = create_db(client)
    drugs = get_drugs_by_defect(drug_collection, prediction)
    print(drugs)
    print(type(drugs))

    # prediction precentage to 2 decimal places
    prediction_percentage = round(prediction_percentage * 100, 2)

    return {"prediction": prediction, "prediction_percentage": prediction_percentage, "drugs": drugs}


# {
#   "prediction": "1. Eczema 1677",
#   "prediction_percentage": 59.1,
#   "drugs": [
#     "Hydrocortisone cream",
#     "Tacrolimus ointment",
#     "Pimecrolimus cream"
#   ]
# }