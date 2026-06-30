import torch
from transformers import PatchTSTConfig, PatchTSTForPrediction

def get_model_prediction(history_tensor, num_features):
    config = PatchTSTConfig(
        context_length=13,
        prediction_length=1,
        num_input_channels=num_features,
        patch_length=4,
        stride=2
    )
    
    model = PatchTSTForPrediction(config)
    
    with torch.no_grad():
        outputs = model(past_values=history_tensor)
        
    predicted_values = outputs.prediction_outputs[0, 0, :].numpy()
    return predicted_values