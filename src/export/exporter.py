from dataclasses import dataclass
from ..format.formatted_model import FormattedModel

@dataclass
class Exporter:
  name: str
  model: FormattedModel

  def export_as_obj(self, filepath: str) -> None:
      """
      Export the model as an OBJ file.
      
      Args:
          filepath (str): The path where the OBJ file should be saved
      """
      with open(filepath, 'w') as f:
          # Write header/comments
          f.write("# Exported OBJ file\n")
          f.write("# Number of vertices: {}\n".format(len(self.model.vertices)))
          f.write("# Number of faces: {}\n\n".format(len(self.model.faces)))
          
          # Write vertices
          for vertex in self.model.vertices:
              # Assuming vertex coordinates are already in appropriate scale
              # If they need scaling, multiply by appropriate factor
              f.write(f"v {vertex.x:.6f} {vertex.y:.6f} {vertex.z:.6f}\n")
          
          # Write faces
          # OBJ files are 1-indexed, so we need to add 1 to all vertex indices
          for face in self.model.faces:
              # Assuming face is a SanitisedFace with v1, v2, v3, v4 attributes
              # If face is triangulated (3 vertices)
              if face.v4 is None:
                  f.write(f"f {face.v1 + 1} {face.v2 + 1} {face.v3 + 1}\n")
              # If face is a quad (4 vertices)
              else:
                  f.write(f"f {face.v1 + 1} {face.v2 + 1} {face.v3 + 1} {face.v4 + 1}\n")