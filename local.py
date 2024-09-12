# def load_model_with_fallback(model_id, controlnet_id):
#     print(f"Attempting to load model: {model_id}")
#     try:
#         pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
#         print("Base model loaded successfully")
#
#         print(f"Attempting to load ControlNet: {controlnet_id}")
#         controlnet = ControlNetModel.from_pretrained(controlnet_id, torch_dtype=torch.float16)
#         pipe.controlnet = controlnet
#         print("ControlNet loaded successfully")
#
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         pipe = pipe.to(device)
#         print(f"Pipeline moved to {device}")
#
#         return pipe
#     except Exception as e:
#         print(f"Error loading model: {str(e)}")
#         return None
#
# def design_room(pipe, empty_room_image: Image.Image, prompt: str, strength: float = 0.75) -> Image.Image:
#     full_prompt = f"Interior design: {prompt}, photorealistic, high quality"
#
#     try:
#         result = pipe(
#             prompt=full_prompt,
#             image=empty_room_image,
#             strength=strength,
#             guidance_scale=7.5,
#         )
#         return result.images[0]
#     except Exception as e:
#         print(f"Error generating image: {str(e)}")
#         return None
#

# controlnet_id = "lllyasviel/sd-controlnet-canny"
#
# pipe = load_model_with_fallback(model_id, controlnet_id)
#
# if pipe is not None:
#     empty_room_path = "empty_room.jpg"
#     if not os.path.exists(empty_room_path):
#         print(f"Error: The file {empty_room_path} does not exist.")
#     else:
#         empty_room = Image.open(empty_room_path)
#         design_prompt = "Modern living room with a grey sofa, glass coffee table, and abstract art on the walls"
#         furnished_room = design_room(pipe, empty_room, design_prompt)
#
#         if furnished_room is not None:
#             furnished_room.save("gen_furnished_room.png")
#             print("Furnished room image saved as 'furnished_room.png'")
# else:
#     print("Failed to load the model. Please check your internet connection and try again.")
