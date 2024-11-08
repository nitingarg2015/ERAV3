import numpy as np
import base64
import os
from imports.baseclass import BaseClass
import trimesh

class ThreeDDataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = trimesh.load(file_path)

    @property
    def contents(self) -> str:
        # returns file name for displaying the image
        return os.path.basename(self.file_path)
    
    # Preprocessing variations
    def preprocess_all(self):
        results = {}
        # Scale the mesh by a factor of 0.5
        scaled_mesh = self.data.copy()
        scaled_mesh.apply_scale(0.5)
        results['scaled'] = self.to_base64(scaled_mesh)

        translated_mesh = self.data.copy()
        translated_mesh.apply_translation([0, 0, 1])
        results['translated'] = self.to_base64(translated_mesh)

        normalized_mesh = self.data.copy()
        normalized_mesh.apply_translation(-normalized_mesh.center_mass)
        normalized_mesh.apply_scale(1.0 / normalized_mesh.extents.max())
        results['normalized'] = self.to_base64(normalized_mesh)

        return results


    # Augmentation variations
    def augment_all(self):
        results = {}

        # Augment Variation 1: Rotate the mesh 90 degrees around the z-axis
        rotated_mesh = self.data.copy()
        rotation_matrix = trimesh.transformations.rotation_matrix(
            angle=np.radians(90), direction=[0, 0, 1], point=rotated_mesh.center_mass
        )
        rotated_mesh.apply_transform(rotation_matrix)
        results['rotated'] = self.to_base64(rotated_mesh)

        # Augment Variation 2: Flip the mesh along the x-axis
        flipped_mesh = self.data.copy()
        flipped_mesh.apply_scale([-1, 1, 1])
        results['flipped'] = self.to_base64(flipped_mesh)

        # Augment Variation 3: Add small random perturbations to vertices
        noisy_mesh = self.data.copy()
        noise = np.random.normal(0, 0.01, noisy_mesh.vertices.shape)
        noisy_mesh.vertices += noise
        results['noisy'] = self.to_base64(noisy_mesh)

        return results

    # Output format: Convert to a web-displayable format
    def to_base64(self, mesh):
        # Convert mesh to a base64 string
        mesh_bytes = mesh.export(file_type='ply')  # or 'stl', 'obj', etc., as required
        return base64.b64encode(mesh_bytes).decode('utf-8')

