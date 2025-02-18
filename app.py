from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.middleware.cors import CORSMiddleware
from utils.mongo_util import create_db, add_data, get_drugs_by_defect, client
from utils.predict import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    try:
        image_path = "test_images/image.jpg"
        with open(image_path, "wb") as buffer:
            buffer.write(file.file.read())

        prediction, prediction_percentage = predict(image_path)
        # defect_collection, drug_collection = create_db(client)
        # drugs = get_drugs_by_defect(drug_collection, prediction)

        prediction_percentage = round(prediction_percentage * 100, 2)
        return {"prediction": prediction, "prediction_percentage": prediction_percentage
            # , "drugs": drugs
                }

    except HTTPException as e:
        return {"error": e.detail}
    except Exception as e:
        return {"error": str(e)}


# {
#   "prediction": "1. Eczema 1677",
#   "prediction_percentage": 59.1,
#   "drugs": [
#     "Hydrocortisone cream",
#     "Tacrolimus ointment",
#     "Pimecrolimus cream"
#   ]
# }