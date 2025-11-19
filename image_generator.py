import requests
import base64
from PIL import Image
from io import BytesIO

class StabilityImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def generate_image(self, prompt, output_file="generated_image.png"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        data = {
            "prompt": (None, prompt),
            "aspect_ratio": (None, "1:1"),
            "output_format": (None, "png")
        }

        response = requests.post(self.endpoint, headers=headers, files=data)

        if response.status_code == 200:
            result = response.json()
            base64_image = result['image']
            image_data = base64.b64decode(base64_image)

            # Save the image to file
            with open(output_file, 'wb') as f:
                f.write(image_data)
            print(f"✅ Image saved as {output_file}")

            # Display the image directly
            image = Image.open(BytesIO(image_data))
            image.show()

        else:
            print("❌ Error:", response.status_code, response.text)


# ------------------- Run Code -------------------
if __name__ == "__main__":
    api_key = "sk-evEuQIbJ7TkwNxcokGqe6xrRgLIgbk73Zx14lEqAC0PFSnMO"  # Replace with your real key
    prompt = input("🖼️ Enter the image description (search prompt): ")

    generator = StabilityImageGenerator(api_key)
    generator.generate_image(prompt)