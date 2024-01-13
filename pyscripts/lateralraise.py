import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import random


pose = mp_pose.Pose()

# Video feed
cap = cv2.VideoCapture(0)

# Counter 
counter = 0
up = False
compliments = ["Awesome", "Excellent", "Fantastic", "Great", "Good", "Super", "Nice", "Amazing", "Perfect", "Terrific"]
random_choice = "Great"
with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.6) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False # Improves Performance

        # Detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Improves Performance

        if results.pose_landmarks:
            points = {}

            for id, lm in enumerate(results.pose_landmarks.landmark):
                height, width, channel = image.shape

                channel_x, channel_y = int(lm.x * width), int(lm.y * height)

                points[id] = (channel_x, channel_y)

            # If elbow above shoulder...
            if not up and points[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1] + 10 <= points[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1] and points[mp_pose.PoseLandmark.LEFT_ELBOW.value][1] + 10 <= points[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]:
                up = True
                counter += 1
                random_choice = random.choice(compliments)
            # if elbow below shoulder...
            elif points[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1] > points[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1] and points[mp_pose.PoseLandmark.LEFT_ELBOW.value][1] > points[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]:
                up = False
                cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                text = "Move the weight out to the side until they reach shoulder height."
                cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)
            elif points[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1] < points[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1] and points[mp_pose.PoseLandmark.LEFT_ELBOW.value][1] < points[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]:
                cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                text = f"{random_choice}! Now move them back to your sides."
                cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)
                
            
            if points[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1] + 85 < points[mp_pose.PoseLandmark.LEFT_ELBOW.value][1]:
                # Right ELBOW is lower than left ELBOW, do something
                cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
                text = "Form Check: Your right arm is higher than your left."
                cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            
            if points[mp_pose.PoseLandmark.LEFT_ELBOW.value][1] + 85 < points[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1]:
                cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
                text = "Form Check: Your left arm is higher than your right."
                cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)


        # Counter text
        cv2.rectangle(image, (0, 0), (225, 73), (51, 68, 255), -1)
        cv2.putText(image, "REPS: ", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

        # Draw connections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(56, 55, 54), thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=(51, 68, 255), thickness=2, circle_radius=2))

        cv2.imshow('Cam', image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()