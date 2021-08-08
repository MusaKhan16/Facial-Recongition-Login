import face_recognition
import cv2
from Facial_Recognition.Error_types import Unavailable_Path
from typing import Callable, List
import time
from File_manager import FileManager
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal


class Face_Client(QThread):
    FACES_PATH = Path("known_faces")
    Success = pyqtSignal(str)
    Failure = pyqtSignal(object)

    def __init__(self, userame: str):
        QThread.__init__(self)
        self.logged_user = userame
        self.webcam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    @property
    def user_photos_path(self):

        if directory_path := FileManager.get_dir(self.FACES_PATH, self.logged_user):
            return directory_path

        raise Unavailable_Path("The path for the users face is unidentified..")

    @property
    def user_images(self):
        return (
            face_recognition.load_image_file(str(path))
            for path in self.user_photos_path.iterdir()
        )

    @property
    def user_image_encodings(self) -> List[int]:
        return [face_recognition.face_encodings(image)[0] for image in self.user_images]

    def run(self):
        """Main loop of the Class, will capture faces."""
        start_time = time.time()

        while True:
            ret, frame = self.webcam.read()

            if not ret:
                break

            minimized_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_minimized_frame = minimized_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_minimized_frame)

            encoded_faces = face_recognition.face_encodings(
                rgb_minimized_frame, face_locations
            )

            for encoded_face in encoded_faces:
                face_matches = face_recognition.compare_faces(
                    self.user_image_encodings, encoded_face
                )

                if any(face_matches):
                    self.Success.emit(self.logged_user)
                    self.webcam.release()
                    self.quit()
                    return

            elapsed_time = time.time()

            if elapsed_time - start_time > 20:
                self.Failure.emit(None)
                self.webcam.release()
                self.quit()
                return
