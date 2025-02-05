from ultralytics import YOLO
import supervision as sv

class Tracker:
    def __init__(self, model_path): #called when we initialize the class
        self.model = YOLO(model_path)
        # each detected object is assigned a unique tracker ID, enabling the continuous following of the object's motion path across different frames
        self.tracker = sv.ByteTrack()
    
    def detect_frames(self, frames):

        batch_size = 20  # stating batch_size as 20. In image processing, working with batches of data can be more efficient than processing each item individually

        detections = []  # initialising an empty list to store all the detection results

        """
        Following loop iterates over the frames in batches. It uses range() with a step size of batch_size, so `i` will take on values 0, 20, 40, etc., until it reaches or exceeds the length of frames
        
        self.model.predict() calls the prediction method of YOLO
        frames[i:i+batch_size] selects a batch of frames from the input.
        conf=0.1 sets a confidence threshold of 0.1 for the detections.
        """
        for i in range(0, len(frames), batch_size):
            detections_batch = self.model.predict(frames[i:i+batch_size], conf=0.1)
            
            # adding the detections from the current batch to the overall detections list.
            detections += detections_batch
            break
        return detections  # returning the detections
    
    def get_object_tracks(self, frames) :
        
        detections = self.detect_frames(frames)
        
        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v:k for k,v in cls_names.items()}
            
            # Convert to supervision detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)
            
            print(detection_supervision)
            break