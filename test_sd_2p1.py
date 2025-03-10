import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from tensor_gui import *

model_id = "stabilityai/stable-diffusion-2-1"

# Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")


visualizer = ModelVisualizer(pipe.unet)
visualizer.register_inc_id_hook(pipe.unet)


prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]
    
image.save("astronaut_rides_horse.png")

gui = GUI(visualizer)
