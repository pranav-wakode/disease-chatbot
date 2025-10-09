import torch

print(f"PyTorch Version: {torch.__version__}")
print("--- Checking for CUDA ---")
is_available = torch.cuda.is_available()
print(f"CUDA Available: {is_available}")

if is_available:
    print(f"CUDA Version (Compiled with by PyTorch): {torch.version.cuda}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    print(f"Current GPU Name: {torch.cuda.get_device_name(0)}")
else:
    print("PyTorch was installed without CUDA support or could not find a compatible GPU.")