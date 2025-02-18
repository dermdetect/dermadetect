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
        image_path = "image.jpg"
        with open(image_path, "wb") as buffer:
            buffer.write(file.file.read())

        print(f"Image saved as {image_path}")
        result = predict(image_path)  # Call predict() and store its returned dictionary

        # Extracting the required fields from the result
        status = result.get("status")
        message = result.get("message")
        label = result.get("label")
        confidence = result.get("confidence")

        # Ensure prediction_percentage is always set
        prediction_percentage = round(confidence * 100, 2) if confidence is not None else None

        if status == "error":
            raise HTTPException(status_code=400, detail=message)

        return {
            "status": status,
            "message": message,
            "label": label,
            "confidence": prediction_percentage,
            # "drugs": drugs  # Uncomment once the drugs feature is implemented
        }

    except HTTPException as e:
        return {
            "status": "error",
            "message": e.detail,
            "label": None,
            "confidence": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "label": None,
            "confidence": None
        }

# {
#   "prediction": "1. Eczema 1677",
#   "prediction_percentage": 59.1,
#   "drugs": [
#     "Hydrocortisone cream",
#     "Tacrolimus ointment",
#     "Pimecrolimus cream"
#   ]
# }
