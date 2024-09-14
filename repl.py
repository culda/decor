import replicate
import requests
import time
from PIL import Image
from io import BytesIO

# Ensure you've set your REPLICATE_API_TOKEN environment variable

def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def object_detection(result, object_type):
    detection = next((result[obj] for obj in result if result[obj]['cls'] == object_type), None)
    
    if detection:
        return detection
    else:
        raise ValueError(f"No {object_type} detected in the image")

def create_mask(image, bbox):
    mask = Image.new('L', image.size, 0)
    for x in range(int(bbox["x0"]), int(bbox["x1"])):
        for y in range(int(bbox["y0"]), int(bbox["y1"])):
            mask.putpixel((x, y), 255)
    return mask

def inpaint_image(image_url, mask_url):
    model = replicate.models.get("stability-ai/sdxl")
    version = model.versions.get("7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc")
    
    return replicate.predictions.create(
        version=version,
        input={
            "prompt": "modern L-shaped red sofa, sleek design, minimalist living room, high-quality leather upholstery, clean lines, contemporary style, vibrant red color, comfortable seating, spacious, well-lit interior, realistic, high resolution",
            "image": image_url,
            "mask": mask_url,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "refine": "expert_ensemble_refiner",
            # "num_inference_steps": 50,
            "scheduler": "K_EULER",
        }
    )

def wait_for_prediction(prediction, timeout=300, poll_interval=10):
    start_time = time.time()
    while prediction.status != "succeeded":
        if time.time() - start_time > timeout:
            raise TimeoutError("Prediction timed out")
        if prediction.status == "failed":
            raise Exception(f"Prediction failed: {prediction.error}")
        print(f"Prediction status: {prediction.status}. Waiting...")
        time.sleep(poll_interval)
        prediction = replicate.predictions.get(prediction.id)
    return prediction.output

def upload_to_imgbb(image):
    api_key = '7c302e151f092a41197c0e53ba3192c4'
    url = 'https://api.imgbb.com/1/upload'
    
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    files = {'image': ('image.png', buffer, 'image/png')}
    data = {'key': api_key}
    response = requests.post(url, files=files, data=data)
    
    return response.json()['data']['url']

img_url = "https://claudiainteriors.co.uk/wp-content/uploads/2020/01/Interiors-with-Art_Canary-Wharf_ClaudiaInteriors10-2048x1366.jpg"

output = {"Det-0": {"x0": 125.7328109741211, "y0": 586.3945922851562, "x1": 2009.5390625, "y1": 1363.78515625, "score": 0.9718478918075562, "cls": "blue sofa"}, "Det-1": {"x0": 257.3641052246094, "y0": 234.32701110839844, "x1": 508.5917053222656, "y1": 474.03521728515625, "score": 0.6458826065063477, "cls": "mao zedong picture"}}

bbox = object_detection(output, "blue sofa")

print(bbox)

img = download_image(img_url)

mask = create_mask(img, bbox)

mask_url = upload_to_imgbb(mask)

print("img", img_url)
print("mask", mask_url)

res = wait_for_prediction(inpaint_image(img_url, mask_url))

print(res)

# output = replicate.run(
#     "zsxkib/yolo-world:d232445620610b78671a7f288f37bf3baec831537503e9064afcf0bfd0f0a151",
#     input={
#         "nms_thr": 0.5,
#         "score_thr": 0.05,
#         "class_names": "blue sofa, mao zedong picture",
#         "input_media": "https://claudiainteriors.co.uk/wp-content/uploads/2020/01/Interiors-with-Art_Canary-Wharf_ClaudiaInteriors10-2048x1366.jpg?v=1585737710",
#         "return_json": True,
#         "max_num_boxes": 100
#     }
# )
# print(output)
# Usage
# img_url = "https://cdn.decoist.com/wp-content/uploads/2015/01/Rustic-dining-room-with-red-table-and-chairs.jpg"
# result_image_url = replace_furniture(img_url)
# print(f"Resulting image URL: {result_image_url}")
