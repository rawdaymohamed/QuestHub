import cloudinary.uploader

def upload_avatar_to_cloudinary(image_file):
    # Upload the image to Cloudinary
    response = cloudinary.uploader.upload(image_file)
    # Return the secure URL of the uploaded image
    return response['secure_url']
