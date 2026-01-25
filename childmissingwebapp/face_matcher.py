import os
from deepface import DeepFace
from django.conf import settings

def match_with_missing_children(uploaded_image_path):
    """
    Compares an uploaded person image with all images inside
    media/child_locator_images/ using DeepFace.
    """

    child_folder = os.path.join(settings.MEDIA_ROOT, "child_locator_images")
    child_images = [os.path.join(child_folder, img) for img in os.listdir(child_folder)]

    for child_img in child_images:
        try:
            result = DeepFace.verify(
                img1_path=uploaded_image_path,
                img2_path=child_img,
                enforce_detection=False
            )

            similarity = 1 - result["distance"]

            if similarity > 0.60:  # threshold for matching
                print("\n============================")
                print("🔴 MATCH FOUND!")
                print(f"Matched With Image: {child_img}")
                print(f"Similarity Score: {similarity}")
                print("============================\n")
                return True

        except Exception as e:
            continue

    return False
