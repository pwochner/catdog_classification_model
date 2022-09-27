import os
import requests
import torch
from torchvision import transforms
import numpy as np
import net


CLASS_LABELS = ["cat", "dog"]


class CatDogClassifier:
    def __init__(self):
        filename = "conv_net_model3.ckpt"
        if not os.path.exists(filename):
            model_path = os.path.join(
                "https://connectionsworkshop.blob.core.windows.net/pets", filename
            )
            r = requests.get(model_path)
            with open(filename, "wb") as outfile:
                outfile.write(r.content)
        self.model = net.CatDogClassifier()
        self.model.load_state_dict(torch.load(filename))
        self.model.eval()

    def predict(self, image):
        # transform input image (as required by model)
        transform_input = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.Normalize(
                    mean=[82.18, 139.30, 140.27], std=[49.40, 35.24, 37.86],
                ),
            ]
        )
        image = image.values
        image = image[:, :, 0:3]  # make sure we have only 3 channels
        image = image / 255  # min/max normalisation
        image = np.transpose(image, (2, 0, 1))
        image = torch.from_numpy(image).type(torch.float32)
        image = image.unsqueeze(0)
        image = transform_input(image)

        # make prediction
        prediction = self.model(image)  # TODO: is it model.predict() for tf?
        prediction = prediction.detach().numpy()
        max_val = np.max(prediction)
        max_ind = np.argmax(prediction)
        return f"{CLASS_LABELS[max_ind]}"

