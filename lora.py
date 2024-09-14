import fal_client

# urlm = fal_client.upload_file("./maskr.png")
# urlc = fal_client.upload_file("./control.png")
# print(urlm, urlc)

# handler = fal_client.submit(
#     "fal-ai/flux-lora-fast-training",
#     arguments={
#         "images_data_url": "https://fal.media/files/lion/1yveiKrb7Dq2kaHWRBI5L.zip",
#         "trigger_word": "ASHLEY-LHF-URB-10",
#     },
# )
#
# result = handler.get()
# print(result)


# handler = fal_client.submit(
#     "fal-ai/flux-general/image-to-image",
#     arguments={
#         "prompt": "Living room with a red ASHLEY-LHF-URB-10 sofa bed in the middle.",
#         "image_url": "https://fal.media/files/penguin/NF-OMVNyVwzNn9e82-MNB.png",
# "loras": [
#     {
#         "path": "https://storage.googleapis.com/fal-flux-lora/1aedf7c073fd430184162386c01b79c7_pytorch_lora_weights.safetensors"
#     }
# ],
#         "controlnets": [
#             {
#                 "path": "lllyasviel/control_v11p_sd15_inpaint",
#                 # "mask_url": "https://fal.media/files/koala/Nf2GQ-CijgY_GDaCrVA3u.png",
#         "control_image_url": "https://fal.media/files/penguin/NF-OMVNyVwzNn9e82-MNB.png",
#             }
#         ],
#     },
# )

handler = fal_client.submit(
    "fal-ai/sdxl-controlnet-union/inpainting",
    arguments={
        "prompt": "Living room with a red ASHLEY-LHF-URB-10 sofa bed in the middle.",
        "image_url": "https://fal.media/files/penguin/NF-OMVNyVwzNn9e82-MNB.png",
        "mask_url": "https://fal.media/files/koala/Nf2GQ-CijgY_GDaCrVA3u.png",
        "loras": [
            {
                "path": "https://decorlora.s3.amazonaws.com/lora.safetensors"
                # "path": "https://storage.googleapis.com/fal-flux-lora/1aedf7c073fd430184162386c01b79c7_pytorch_lora_weights.safetensors"
            }
        ],
    },
)

result = handler.get()
print(result)
