import openai
openai.api_key = "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"  # supply your API key however you choose

image_resp = openai.Image.create(prompt="two dogs playing chess, oil painting", n=4, size="512x512")
