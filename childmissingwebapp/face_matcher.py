import os
from django.conf import settings

# Prevent TensorFlow from allocating GPU resources and reduce logs
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def match_with_missing_children(uploaded_image_path):
    """
    Compares an uploaded person image with all images inside
    media/child_locator_images/ using the highly accurate Facenet512 model.
    """
    # Lazy import to prevent importing TensorFlow/DeepFace at Django startup
    from deepface import DeepFace

    child_folder = os.path.join(settings.MEDIA_ROOT, "child_locator_images")
    
    # Ensure the directory exists to prevent errors
    if not os.path.exists(child_folder):
        print(f"Error: Folder {child_folder} not found.")
        return False

    child_images = [
        os.path.join(child_folder, img) for img in os.listdir(child_folder) 
        if img.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    for child_img in child_images:
        try:
            # Facenet512 is more precise for child facial features than the default model
            # RetinaFace is superior for detecting faces at various angles (common in CCTV/Social Media)
            result = DeepFace.verify(
                img1_path=uploaded_image_path,
                img2_path=child_img,
                model_name="Facenet512",
                detector_backend="retinaface",
                enforce_detection=False,
                distance_metric="cosine"
            )

            # result["verified"] uses the model's mathematically optimal threshold
            if result["verified"]:
                similarity = 1 - result["distance"]
                print("\n============================")
                print("🔴 MATCH FOUND!")
                print(f"Matched With Image: {os.path.basename(child_img)}")
                print(f"Confidence Score: {similarity:.4f}")
                print(f"Model Used: Facenet512")
                print("============================\n")
                return True

        except Exception as e:
            print(f"Error processing {child_img}: {str(e)}")
            continue

    return False