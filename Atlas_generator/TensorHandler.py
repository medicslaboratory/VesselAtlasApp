import nibabel as nib
import numpy as np


class VesselAtlas:
    def __init__(self, age: float, sex_female: bool, tensor_dir = '..', save: bool = False):
        self.age_estimate = nib.load(f'{tensor_dir}/Age_estimate.mnc')
        self.intercept_estimate = nib.load(f'{tensor_dir}/Intercept_estimate.mnc')
        self.sex_estimate = nib.load(f'{tensor_dir}/Sex_estimate.mnc')
        self.sex_female = int(sex_female)
        self.age = age
        self.atlas_tensor = self.compute_atlas()
        if save:
            nib.save(self.atlas_tensor, f'Atlas_Age_{age}_{"Female" if sex_female else "Male"}.mnc')

    def compute_atlas(self):
        tensor_age_estimate = self.age_estimate.get_fdata()
        tensor_intercept_estimate = self.intercept_estimate.get_fdata()
        tensor_sex_estimate = self.sex_estimate.get_fdata()
        return tensor_intercept_estimate + self.age * tensor_age_estimate + (self.sex_female + 1)*tensor_sex_estimate


if __name__ == '__main__':
    tensor = nib.load('../Atlas_Age_20_Male.mnc').get_fdata()
    tensor_2 = VesselAtlas(20, False).atlas_tensor
    print(np.allclose(tensor, tensor_2))
