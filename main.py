from huggingface_hub import InferenceClient
from PIL import Image
import io


def generate_image(input_image_path, prompt):
    # Initialize the InferenceClient
    client = InferenceClient(
        model="lllyasviel/sd-controlnet-canny",
        token="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",
    )

    # Open and read the input image
    with open(input_image_path, "rb") as f:
        input_image = f.read()

    # Set up the parameters
    params = {
        "prompt": prompt,
        "strength": 0.75,
        "guidance_scale": 7.5,
        "negative_prompt": "blurry, low quality, ugly",
    }

    # Make the API call
    # response = client.image_to_image(
    #     model="stabilityai/stable-diffusion-2-1",
    #     image=input_image,
    #     **params
    # )

    response = client.image_to_image(
        "empty_room.jpg",
        prompt="Modern living room with a grey sofa, glass coffee table, and abstract art on the walls",
    )

    return response


# Parameters
input_image_path = "empty_room.jpg"
prompt = "Modern living room with a grey sofa, glass coffee table, and abstract art on the walls"

# Generate the image
try:
    generated_image = generate_image(input_image_path, prompt)
    print(generated_image)

    # Save the generated image directly
    generated_image.save("furnished_room.png")
    print("Image saved as furnished_room.png")
except Exception as e:
    print(f"An error occurred: {str(e)}")
