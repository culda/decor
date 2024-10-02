import torch
from diffusers.utils import load_image
from diffusers.pipelines.flux.pipeline_flux_controlnet_inpaint import FluxControlNetInpaintPipeline
from diffusers.models.controlnet_flux import FluxControlNetModel
from controlnet_aux import CannyDetector

base_model = 'black-forest-labs/FLUX.1-dev'
controlnet_model = 'YishaoAI/flux-dev-controlnet-canny-kid-clothes'

pipe = FluxControlNetInpaintPipeline.from_pretrained(base_model, controlnet=controlnet, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power
pipe.to("cuda")

image = load_image(image_path)
mask = load_image(mask_path)
canny = CannyDetector()
canny_image = canny(image)
prompt = "children's clothing model"

image_res = pipe(
    prompt,
    image=image,
    control_image=canny_image,
    controlnet_conditioning_scale=0.5,
    mask_image=mask,
    strength=0.95,
    num_inference_steps=50,
    guidance_scale=5,
    generator=generator,
    joint_attention_kwargs={"scale": 0.8},
    ).images[0]
