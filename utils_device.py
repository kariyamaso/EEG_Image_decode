import torch

def get_device(device_arg='auto'):
    """
    Get the appropriate device for PyTorch operations.
    
    Args:
        device_arg (str): Device specification. Options:
            - 'auto': Automatically select best available (mps > cuda > cpu)
            - 'mps': Force MPS (Metal Performance Shaders) on Mac
            - 'cuda:X': Use CUDA device X
            - 'cpu': Force CPU
    
    Returns:
        torch.device: The selected device
    """
    if device_arg == 'auto':
        if torch.backends.mps.is_available() and torch.backends.mps.is_built():
            return torch.device('mps')
        elif torch.cuda.is_available():
            return torch.device('cuda')
        else:
            return torch.device('cpu')
    elif device_arg == 'mps':
        if torch.backends.mps.is_available() and torch.backends.mps.is_built():
            return torch.device('mps')
        else:
            print("MPS not available, falling back to CPU")
            return torch.device('cpu')
    elif device_arg.startswith('cuda'):
        if torch.cuda.is_available():
            return torch.device(device_arg)
        else:
            print(f"CUDA not available, falling back to CPU")
            return torch.device('cpu')
    else:
        return torch.device('cpu')

def print_device_info(device):
    """Print information about the selected device."""
    if device.type == 'mps':
        print(f"Using MPS (Metal Performance Shaders) on Mac GPU")
    elif device.type == 'cuda':
        print(f"Using CUDA device: {torch.cuda.get_device_name(device)}")
    else:
        print(f"Using CPU")