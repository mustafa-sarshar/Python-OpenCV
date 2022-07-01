"""
Main Source: https://www.youtube.com/watch?v=-toNMaS4SeQ&ab_channel=NicolaiNielsen-ComputerVision%26AI
"""
import cv2 as cv
import cv2
import mediapipe as mp
import numpy as np
import time

from pyparsing import col

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    time_start = time.perf_counter()        # OR time_start = time.time()

    frame = cv.cvtColor(cv2.flip(frame, 1), cv.COLOR_BGR2RGB)
    frame.flags.writeable = False           # To improve performance    
    results = face_mesh.process(frame)      # Get the result    
    frame.flags.writeable = True            # To improve performance
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    
    img_h, img_w, img_c = frame.shape
    face_3d = []
    face_2d = []
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for lm_id, lm in enumerate(face_landmarks.landmark):
                if lm_id == 33 or lm_id == 263 or lm_id == 1 or lm_id == 61 or lm_id == 291 or lm_id == 199:
                    if lm_id == 1:
                        nose_2d = (lm.x*img_w, lm.y*img_h)
                        nose_3d = (lm.x*img_w, lm.y*img_h, lm.z*3000)
                    x, y = int(lm.x*img_w), int(lm.y*img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])
                    
                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])
                    
            # Convert it to the Numpy array
            face_2d = np.array(face_2d, dtype=np.float64)
            
            # Convert it to the Numpy array
            face_3d = np.array(face_3d, dtype=np.float64)
            
            # The camera matrix
            focal_length = 1 * img_w
            
            cam_matrix = np.array([
                [focal_length, 0,            img_h/2],
                [0,            focal_length, img_w/2],
                [0,            0,            1      ],
            ])
            
            # The distortaion parameters
            dist_matrix = np.zeros((4, 1), dtype=np.float64)
            
            # Solve PnP
            success, rot_vec, trans_vec = cv.solvePnP(objectPoints=face_3d, imagePoints=face_2d, cameraMatrix=cam_matrix, distCoeffs=dist_matrix)
            
            # Get Rotational Matrix
            rmat, jac = cv.Rodrigues(rot_vec)
            
            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv.RQDecomp3x3(rmat)
            angles = np.array(angles)
            
            # Get the y rotation degree
            # angle_x = angles[0] * 360
            angle_x = np.rad2deg(angles[0])
            # angle_y = angles[1] * 360
            angle_y = np.rad2deg(angles[1])
            # angle_z = angles[2] * 360
            angle_z = np.rad2deg(angles[2])
            
            # Estimate the tilt of the head
            sensitivity_factor = 1
            if angle_y < -1*sensitivity_factor:
                head_tilt = "Looking Left"
            elif angle_y > 1*sensitivity_factor:
                head_tilt = "Looking Right"
            elif angle_x < -1*sensitivity_factor:
                head_tilt = "Looking Down"
            elif angle_x > 1*sensitivity_factor:
                head_tilt = "Looking Up"
            else:
                head_tilt = "Looking Forward"
            
            # print(head_tilt)
            
            # Display the nose direction
            nose_3d_projection, jacobian = cv.projectPoints(
                objectPoints=nose_3d,
                rvec=rot_vec,
                tvec=trans_vec,
                cameraMatrix=cam_matrix,
                distCoeffs=dist_matrix,
            )
            
            nose_scale_factor = 10
            nose_thickness = 3
            nose_color = (255, 0, 0)
            pt1 = (int(nose_2d[0]), int(nose_2d[1]))
            pt2 = (int(nose_2d[0]+angle_y*nose_scale_factor), int(nose_2d[1]-angle_x*nose_scale_factor))
            cv.line(img=frame, pt1=pt1, pt2=pt2, color=nose_color, thickness=nose_thickness)
            
            # Display the results in Text format
            cv.putText(img=frame, text=head_tilt, org=(20, 50), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=.7, color=(0, 255, 0), thickness=2)
            cv.putText(img=frame, text=f"Angle (X): {angle_x:.2f}", org=(500, 50), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=(0, 0, 255), thickness=2)
            cv.putText(img=frame, text=f"Angle (Y): {angle_y:.2f}", org=(500, 70), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=(0, 0, 255), thickness=2)
            cv.putText(img=frame, text=f"Angle (Z): {angle_z:.2f}", org=(500, 90), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=(0, 0, 255), thickness=2)
            
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            # connections=mp_face_mesh.FACEMESH_TESSELATION,
            connections=None,
            # landmark_drawing_spec=drawing_spec,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_spec,
        )

    time_end = time.perf_counter()      # OR time_end = time.time()
    time_total = time_end - time_start
    # print(f"Total Time: {time_total:.4f}, FPS: {fps:.2f}")
    cv.putText(img=frame, text=f"fps: {(1/time_total):.2f}", org=(20, 450), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=.7, color=(0, 255, 0), thickness=2)
        
    cv.imshow("Head Pose Estimation", frame)
    if cv.waitKey(5) & 0xFF == 27:
        break

cap.release()
