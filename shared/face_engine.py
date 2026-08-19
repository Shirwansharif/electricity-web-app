"""
Face Recognition Engine - Core Module
سیستەمی ناسینەوەی دەموچاو

This module handles all face recognition operations including:
- Face detection
- Face encoding
- Face recognition
- Database management
"""

import face_recognition
import cv2
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FaceRecognitionEngine:
    """Core engine for face recognition operations"""
    
    def __init__(self, data_dir: str = "data/faces"):
        """
        Initialize the face recognition engine
        
        Args:
            data_dir: Directory to store face encodings database
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.data_dir / "faces_db.pkl"
        
        # Database structure: {"person_name": {"encodings": [...], "metadata": {...}}}
        self.known_faces = {}
        self.load_database()
        
    def load_database(self):
        """Load face encodings from database file"""
        try:
            if self.db_file.exists():
                with open(self.db_file, 'rb') as f:
                    self.known_faces = pickle.load(f)
                logger.info(f"✅ Loaded {len(self.known_faces)} people from database")
            else:
                logger.info("📝 Creating new face database")
                self.known_faces = {}
        except Exception as e:
            logger.error(f"❌ Error loading database: {e}")
            self.known_faces = {}
    
    def save_database(self):
        """Save face encodings to database file"""
        try:
            with open(self.db_file, 'wb') as f:
                pickle.dump(self.known_faces, f)
            logger.info("✅ Database saved successfully")
        except Exception as e:
            logger.error(f"❌ Error saving database: {e}")
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            List of face locations as (top, right, bottom, left) tuples
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image, model="hog")
        return face_locations
    
    def encode_face(self, image: np.ndarray, face_location: Optional[Tuple] = None) -> Optional[np.ndarray]:
        """
        Generate face encoding for a detected face
        
        Args:
            image: Input image as numpy array (BGR format)
            face_location: Optional face location tuple (top, right, bottom, left)
            
        Returns:
            Face encoding as numpy array, or None if no face found
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Get encoding
        if face_location:
            encodings = face_recognition.face_encodings(rgb_image, [face_location])
        else:
            encodings = face_recognition.face_encodings(rgb_image)
        
        if len(encodings) > 0:
            return encodings[0]
        return None
    
    def add_person(self, name: str, image: np.ndarray, metadata: Optional[Dict] = None) -> bool:
        """
        Add a new person to the database
        
        Args:
            name: Person's name
            image: Image containing the person's face (BGR format)
            metadata: Optional metadata (e.g., date added, notes)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Detect face
            face_locations = self.detect_faces(image)
            if len(face_locations) == 0:
                logger.warning(f"⚠️ No face detected for {name}")
                return False
            
            if len(face_locations) > 1:
                logger.warning(f"⚠️ Multiple faces detected for {name}, using the first one")
            
            # Encode face
            encoding = self.encode_face(image, face_locations[0])
            if encoding is None:
                logger.warning(f"⚠️ Could not encode face for {name}")
                return False
            
            # Add to database
            if name not in self.known_faces:
                self.known_faces[name] = {"encodings": [], "metadata": metadata or {}}
            
            self.known_faces[name]["encodings"].append(encoding)
            self.save_database()
            
            logger.info(f"✅ Added {name} to database")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding person {name}: {e}")
            return False
    
    def recognize_faces(self, image: np.ndarray, tolerance: float = 0.6) -> List[Dict]:
        """
        Recognize faces in an image
        
        Args:
            image: Input image as numpy array (BGR format)
            tolerance: Face matching tolerance (lower is more strict)
            
        Returns:
            List of dictionaries containing recognition results
        """
        results = []
        
        try:
            # Detect faces
            face_locations = self.detect_faces(image)
            if len(face_locations) == 0:
                return results
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Encode all detected faces
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            # Compare with known faces
            for face_encoding, face_location in zip(face_encodings, face_locations):
                name = "Unknown"
                confidence = 0.0
                
                # Compare with each person in database
                for person_name, person_data in self.known_faces.items():
                    # Compare with all encodings for this person
                    matches = face_recognition.compare_faces(
                        person_data["encodings"],
                        face_encoding,
                        tolerance=tolerance
                    )
                    
                    if True in matches:
                        # Calculate confidence based on face distance
                        face_distances = face_recognition.face_distance(
                            person_data["encodings"],
                            face_encoding
                        )
                        best_match_distance = min(face_distances)
                        confidence = max(0, 1 - best_match_distance)
                        
                        if confidence > 0.4:  # Minimum confidence threshold
                            name = person_name
                            break
                
                results.append({
                    "name": name,
                    "confidence": confidence,
                    "location": face_location,
                    "box": {
                        "top": face_location[0],
                        "right": face_location[1],
                        "bottom": face_location[2],
                        "left": face_location[3]
                    }
                })
            
        except Exception as e:
            logger.error(f"❌ Error recognizing faces: {e}")
        
        return results
    
    def delete_person(self, name: str) -> bool:
        """
        Delete a person from the database
        
        Args:
            name: Person's name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if name in self.known_faces:
                del self.known_faces[name]
                self.save_database()
                logger.info(f"✅ Deleted {name} from database")
                return True
            else:
                logger.warning(f"⚠️ {name} not found in database")
                return False
        except Exception as e:
            logger.error(f"❌ Error deleting person {name}: {e}")
            return False
    
    def get_all_people(self) -> List[str]:
        """Get list of all people in database"""
        return list(self.known_faces.keys())
    
    def get_person_info(self, name: str) -> Optional[Dict]:
        """Get information about a specific person"""
        return self.known_faces.get(name)
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        total_encodings = sum(len(data["encodings"]) for data in self.known_faces.values())
        return {
            "total_faces": total_encodings,
            "unique_people": len(self.known_faces),
            "database_size": self.db_file.stat().st_size if self.db_file.exists() else 0
        }
    
    def draw_results(self, image: np.ndarray, results: List[Dict]) -> np.ndarray:
        """
        Draw recognition results on image
        
        Args:
            image: Input image as numpy array (BGR format)
            results: Recognition results from recognize_faces()
            
        Returns:
            Image with drawn boxes and labels
        """
        output_image = image.copy()
        
        for result in results:
            top, right, bottom, left = result["location"]
            name = result["name"]
            confidence = result["confidence"]
            
            # Choose color based on recognition
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            
            # Draw box
            cv2.rectangle(output_image, (left, top), (right, bottom), color, 2)
            
            # Draw label
            label = f"{name}"
            if name != "Unknown":
                label += f" ({confidence:.2%})"
            
            cv2.rectangle(output_image, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
            cv2.putText(output_image, label, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        return output_image
