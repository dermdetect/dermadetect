from utils.predict import predict
from utils.mongo_util import create_db, add_data, get_drugs_by_defect, client

data_path = r"D:\Projects\skincare\dataset\IMG_CLASSES\1. Eczema 1677"
image_name = "0_1.jpg"

image_path = data_path + "/" + image_name

prediction, precentage = predict(image_path)
print(prediction)
print(precentage)


defect_collection, drug_collection = create_db(client)
# add_data(defect_collection, drug_collection)
print(get_drugs_by_defect(drug_collection, prediction))
# delete_all_data(defect_collection, drug_collection)
