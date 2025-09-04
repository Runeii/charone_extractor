import json
import os
from typing import Dict, List
from src.construct.constructed_animation import ConstructedAnimation


class AnimationHashManager:
    """Manages animation hashing and JSON file tracking for deduplication."""
    
    def __init__(self, output_folder: str):
        """Initialize the animation hash manager.
        
        Args:
            output_folder: Base output folder for hash file and animations folder
        """
        self.output_folder = output_folder
        self.animation_hash_file = os.path.join(output_folder, "animation_hash.json")
        self.animations_folder = os.path.join(output_folder, "animations")
        
        # Ensure the animations folder exists
        os.makedirs(self.animations_folder, exist_ok=True)
        
        # Load existing hash data
        self.hash_data = self._load_hash_data()
    
    def _load_hash_data(self) -> Dict[str, Dict[str, List[str]]]:
        """Load the animation hash data from JSON file.
        
        Returns:
            Dictionary with structure: {map_name: {model_name: [hash1, hash2, ...]}}
        """
        if os.path.exists(self.animation_hash_file):
            try:
                with open(self.animation_hash_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load animation hash file: {e}")
                return {}
        return {}
    
    def _save_hash_data(self) -> None:
        """Save the animation hash data to JSON file."""
        try:
            with open(self.animation_hash_file, 'w') as f:
                json.dump(self.hash_data, f, indent=2, sort_keys=True)
        except IOError as e:
            print(f"Error: Could not save animation hash file: {e}")
    
    def get_animation_hash(self, animation: ConstructedAnimation) -> str:
        """Get the hash for an animation.
        
        Args:
            animation: The constructed animation to hash
            
        Returns:
            str: The SHA256 hash of the animation data
        """
        return animation.get_data_hash()
    
    def is_animation_saved(self, animation_hash: str) -> bool:
        """Check if an animation with this hash is already saved.
        
        Args:
            animation_hash: The hash to check
            
        Returns:
            bool: True if animation file exists
        """
        animation_path = os.path.join(self.animations_folder, f"{animation_hash}.blend")
        return os.path.exists(animation_path)
    
    def get_animation_file_path(self, animation_hash: str) -> str:
        """Get the file path for an animation based on its hash.
        
        Args:
            animation_hash: The hash of the animation
            
        Returns:
            str: Full path where the animation should be saved
        """
        return os.path.join(self.animations_folder, f"{animation_hash}.blend")
    
    def add_animation_to_model(self, map_name: str, model_name: str, animation_hash: str) -> None:
        """Add an animation hash to a model's list for a specific map.
        
        Args:
            map_name: Name of the map
            model_name: Name of the model
            animation_hash: Hash of the animation to add
        """
        if map_name not in self.hash_data:
            self.hash_data[map_name] = {}
        
        if model_name not in self.hash_data[map_name]:
            self.hash_data[map_name][model_name] = []
        
        if animation_hash not in self.hash_data[map_name][model_name]:
            self.hash_data[map_name][model_name].append(animation_hash)
            self._save_hash_data()
    
    def get_model_animations(self, map_name: str, model_name: str) -> List[str]:
        """Get all animation hashes for a specific model in a map.
        
        Args:
            map_name: Name of the map
            model_name: Name of the model
            
        Returns:
            List[str]: List of animation hashes for the model
        """
        return self.hash_data.get(map_name, {}).get(model_name, [])
    
    def process_animations_for_model(self, map_name: str, model_name: str, animations: List[ConstructedAnimation]) -> List[Dict[str, any]]:
        """Process animations for a model and return hash information.
        
        Args:
            map_name: Name of the map
            model_name: Name of the model
            animations: List of constructed animations to process
            
        Returns:
            List[Dict[str, str]]: List of dictionaries with animation info:
                [{"original_name": str, "hash": str, "exists": bool, "file_path": str}, ...]
        """
        animation_info = []
        
        for animation in animations:
            animation_hash = self.get_animation_hash(animation)
            exists = self.is_animation_saved(animation_hash)
            
            # Add to hash mapping
            self.add_animation_to_model(map_name, model_name, animation_hash)
            
            animation_info.append({
                "original_name": animation.name,
                "hash": animation_hash,
                "exists": exists,
                "file_path": self.get_animation_file_path(animation_hash)
            })
            
            if exists:
                print(f"Animation already exists: {animation.name} -> {animation_hash}")
            else:
                print(f"New animation detected: {animation.name} -> {animation_hash}")
        
        return animation_info
