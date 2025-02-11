from pymongo.mongo_client import MongoClient

# load from .env
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def create_db(client):
    # Create a new database named 'skincare'
    db = client['skincare']

    # Create a collection named 'defect' in the 'skincare' database.
    defect_collection = db['defect']

    # Create a collection named 'drug' in the 'skincare' database.
    drug_collection = db['drug']

    return defect_collection, drug_collection


def add_data(defect_collection, drug_collection):
    # '1. Eczema 1677',
    # '10. Warts Molluscum and other Viral Infections - 2103',
    # '2. Melanoma 15.75k',
    # '3. Atopic Dermatitis - 1.25k',
    # '4. Basal Cell Carcinoma (BCC) 3323',
    # '5. Melanocytic Nevi (NV) - 7970',
    # '6. Benign Keratosis-like Lesions (BKL) 2624',
    # '7. Psoriasis pictures Lichen Planus and related diseases - 2k',
    # '8. Seborrheic Keratoses and other Benign Tumors - 1.8k',
    # '9. Tinea Ringworm Candidiasis and other Fungal Infections - 1.7k'

    # Eczema: Hydrocortisone cream, Tacrolimus ointment, Pimecrolimus cream.
    # Melanoma: Dabrafenib, Trametinib, Pembrolizumab.
    # Atopic Dermatitis: Calcineurin inhibitors, Topical corticosteroids, PDE4 inhibitors.
    # Basal Cell Carcinoma (BCC): Imiquimod cream, Fluorouracil cream, Photodynamic therapy.
    # Melanocytic Nevi (NV): Cryotherapy, Laser therapy, Excision.
    # Benign Keratosis-like Lesions (BKL): Cryotherapy, Curettage and electrodesiccation, Laser therapy.
    # Psoriasis pictures Lichen Planus and related diseases: Topical corticosteroids, Vitamin D analogues, Retinoids.
    # Seborrheic Keratoses and other Benign Tumors: Cryotherapy, Curettage and electrodesiccation, Laser therapy.
    # Tinea Ringworm Candidiasis and other Fungal Infections: Antifungal creams, Antifungal pills, Antifungal shampoos.
    # '10. Warts Molluscum and other Viral Infections - 2103': Acyclovir, Imiquimoid, Podofilox

    defect_data = [
        {'name': '1. Eczema 1677'},
        {'name': '10. Warts Molluscum and other Viral Infections - 2103'},
        {'name': '2. Melanoma 15.75k'},
        {'name': '3. Atopic Dermatitis - 1.25k'},
        {'name': '4. Basal Cell Carcinoma (BCC) 3323'},
        {'name': '5. Melanocytic Nevi (NV) - 7970'},
        {'name': '6. Benign Keratosis-like Lesions (BKL) 2624'},
        {'name': '7. Psoriasis pictures Lichen Planus and related diseases - 2k'},
        {'name': '8. Seborrheic Keratoses and other Benign Tumors - 1.8k'},
        {'name': '9. Tinea Ringworm Candidiasis and other Fungal Infections - 1.7k'}
    ]
    defect_collection.insert_many(defect_data)

    # Add dummy data to the 'drug' collection.
    drug_data = [
        {'name': 'Hydrocortisone cream', 'defect_name': '1. Eczema 1677'},
        {'name': 'Tacrolimus ointment', 'defect_name': '1. Eczema 1677'},
        {'name': 'Pimecrolimus cream', 'defect_name': '1. Eczema 1677'},
        {'name': 'Dabrafenib', 'defect_name': '2. Melanoma 15.75k'},
        {'name': 'Trametinib', 'defect_name': '2. Melanoma 15.75k'},
        {'name': 'Pembrolizumab', 'defect_name': '2. Melanoma 15.75k'},
        {'name': 'Calcineurin inhibitors', 'defect_name': '3. Atopic Dermatitis - 1.25k'},
        {'name': 'Topical corticosteroids', 'defect_name': '3. Atopic Dermatitis - 1.25k'},
        {'name': 'PDE4 inhibitors', 'defect_name': '3. Atopic Dermatitis - 1.25k'},
        {'name': 'Imiquimod cream', 'defect_name': '4. Basal Cell Carcinoma (BCC) 3323'},
        {'name': 'Fluorouracil cream', 'defect_name': '4. Basal Cell Carcinoma (BCC) 3323'},
        {'name': 'Photodynamic therapy', 'defect_name': '4. Basal Cell Carcinoma (BCC) 3323'},
        {'name': 'Cryotherapy', 'defect_name': '5. Melanocytic Nevi (NV) - 7970'},
        {'name': 'Laser therapy', 'defect_name': '5. Melanocytic Nevi (NV) - 7970'},
        {'name': 'Excision', 'defect_name': '5. Melanocytic Nevi (NV) - 7970'},
        {'name': 'Cryotherapy', 'defect_name': '6. Benign Keratosis-like Lesions (BKL) 2624'},
        {'name': 'Curettage and electrodesiccation', 'defect_name': '6. Benign Keratosis-like Lesions (BKL) 2624'},
        {'name': 'Laser therapy', 'defect_name': '6. Benign Keratosis-like Lesions (BKL) 2624'},
        {'name': 'Topical corticosteroids',
         'defect_name': '7. Psoriasis pictures Lichen Planus and related diseases - 2k'},
        {'name': 'Vitamin D analogues', 'defect_name': '7. Psoriasis pictures Lichen Planus and related diseases - 2k'},
        {'name': 'Retinoids', 'defect_name': '7. Psoriasis pictures Lichen Planus and related diseases - 2k'},
        {'name': 'Cryotherapy', 'defect_name': '8. Seborrheic Keratoses and other Benign Tumors - 1.8k'},
        {'name': 'Curettage and electrodesiccation',
         'defect_name': '8. Seborrheic Keratoses and other Benign Tumors - 1.8k'},
        {'name': 'Laser therapy', 'defect_name': '8. Seborrheic Keratoses and other Benign Tumors - 1.8k'},
        {'name': 'Antifungal creams',
         'defect_name': '9. Tinea Ringworm Candidiasis and other Fungal Infections - 1.7k'},
        {'name': 'Antifungal pills', 'defect_name': '9. Tinea Ringworm Candidiasis and other Fungal Infections - 1.7k'},
        {'name': 'Antifungal shampoos',
         'defect_name': '9. Tinea Ringworm Candidiasis and other Fungal Infections - 1.7k'},
        {'name': 'Acyclovir', 'defect_name': '10. Warts Molluscum and other Viral Infections - 2103'},
        {'name': 'Imiquimoid', 'defect_name': '10. Warts Molluscum and other Viral Infections - 2103'},
        {'name': 'Podofilox', 'defect_name': '10. Warts Molluscum and other Viral Infections - 2103'}
    ]
    drug_collection.insert_many(drug_data)


def get_drugs_by_defect(drug_collection, defect_name):
    result = drug_collection.find({'defect_name': defect_name})
    drugs = []
    for r in result:
        drugs.append(r['name'])
    return drugs


# delete all data
def delete_all_data(defect_collection, drug_collection):
    defect_collection.delete_many({})
    drug_collection.delete_many({})
