import boto3
from PIL import Image
import sys

# Initialize S3 client
s3 = boto3.client("s3")

# I DID THAT WITH A AWS PLAYGROUND TO SEE IF IT WORKS, you have to set up your own credentials.
# Initialize S3 client with credentials
# s3 = boto3.client(
#     's3',
#     aws_access_key_id='AKIA6I5UQEESTORXZSM4',
#     aws_secret_access_key='Uz7rK0GZoCOzYi+mpm4DJ4lGz0AYlYhvahQmRD5Q',
#     region_name='us-east-1'
# )

# Set source and destination S3 bucket names

if len(sys.argv) < 3:
    print("Usage: python s3_buckets.py [src_bucket_name] [dst_bucket_name]")
    sys.exit(1)
src_bucket_name = sys.argv[1]
dst_bucket_name = sys.argv[2]

# Set log file name
log_file = "transparent-images.txt"

# Get list of all objects in the source S3 bucket
result = s3.list_objects(Bucket=src_bucket_name)

# Open log file
with open(log_file, "w") as log:
    for content in result.get("Contents"):
        # The "Key" attritube contains the name of the image.
        image_file = content.get("Key")
        # open the image using PIL with a try/expect in case there is a problem to open the image.
        try:
            img = Image.open(
                s3.get_object(Bucket=src_bucket_name, Key=image_file)["Body"]
            )
        except Exception as e:
            print(f"Error opening image: {image_file}. Error: {e}")
        # check if the image is already RGBA, if it's not convert it.
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        # Get a list of all pixels in the image and then get the alpha values only to check for transparency.
        pixels = list(img.getdata())
        alpha_values = [pixel[3] for pixel in pixels]
        # Loop through the list of alpha values.
        for alpha in alpha_values:
            # Check if the alpha has an alpha value less than 255, (255 is the maximum alpha value, which means the pixel is fully opaque)
            if alpha < 255:
                # The pixel is transparent
                print(f"Transparent pixel found in the image: {image_file}!")
                # Log image file name to the log file
                log.write(f"{image_file}\n")
                break
        else:
            print(f"No transparent pixels were found in image: {image_file}.")
            try:
                # Copy image file to the destination S3 bucket if it has no transparent pixels
                s3.copy_object(
                    Bucket=dst_bucket_name,
                    CopySource={"Bucket": src_bucket_name, "Key": image_file},
                    Key=image_file,
                )
            except Exception as e:
                print(f"Error copying image: {image_file}. Error: {e}")
