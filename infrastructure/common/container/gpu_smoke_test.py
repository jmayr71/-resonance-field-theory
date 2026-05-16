import os
import platform
import torch

print("RFT GPU smoke test")
print("==================")
print("python platform:", platform.platform())
print("torch version:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
print("RFT_REPO:", os.environ.get("RFT_REPO"))
print("RFT_RUNS:", os.environ.get("RFT_RUNS"))
print("RFT_ARTIFACTS:", os.environ.get("RFT_ARTIFACTS"))

if torch.cuda.is_available():
    print("device count:", torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(f"device {i}:", torch.cuda.get_device_name(i))
    x = torch.randn((4096, 4096), device="cuda")
    y = x @ x.T
    torch.cuda.synchronize()
    print("matrix result:", float(y[0, 0].detach().cpu()))
else:
    raise SystemExit("CUDA is not available. Check GPU driver and NVIDIA container runtime.")
