import numpy as np
from skimage import measure
from pyvox.parser import VoxParser
import trimesh

# .vox 파일을 읽어오는 함수
def load_vox_file(file_path):
    parser = VoxParser(file_path)
    vox_data = parser.parse()
    size = vox_data.models[0].size
    voxels = vox_data.models[0].voxels

    # 복셀 배열을 3D numpy 배열로 변환
    voxel_array = np.zeros((size.z, size.y, size.x), dtype=bool)
    for voxel in voxels:
        voxel_array[voxel.z, voxel.y, voxel.x] = True

    return voxel_array

# 마칭 큐브를 적용하는 함수
def apply_marching_cubes(voxel_array):
    # 마칭 큐브 적용 (등고 값은 0.5로 설정)
    verts, faces, normals, values = measure.marching_cubes(voxel_array, level=0.5)
    return verts, faces

# 면의 정점 순서를 뒤집는 함수 (면 반전)
def invert_faces(faces):
    return np.fliplr(faces)  # 면을 반전 (정점 순서를 뒤집음)

# 회전 행렬 적용 함수
def rotate_vertices(verts, angle_degrees, axis='z'):
    angle_radians = np.radians(angle_degrees)
    
    # Z축 기준 회전 (기본적으로 Z축 회전으로 설정)
    if axis == 'z':
        rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians), 0],
                                    [np.sin(angle_radians), np.cos(angle_radians), 0],
                                    [0, 0, 1]])
    elif axis == 'y':
        rotation_matrix = np.array([[np.cos(angle_radians), 0, np.sin(angle_radians)],
                                    [0, 1, 0],
                                    [-np.sin(angle_radians), 0, np.cos(angle_radians)]])
    elif axis == 'x':
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle_radians), -np.sin(angle_radians)],
                                    [0, np.sin(angle_radians), np.cos(angle_radians)]])

    rotated_verts = np.dot(verts, rotation_matrix.T)
    return rotated_verts

# 파일로 저장하는 함수 (PLY 형식)
def save_as_ply(verts, faces, output_path):
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    mesh.export(output_path)

# 파일 경로 설정 및 실행
vox_file_path = "./parsing_sphere/sphere_voxel.vox"
output_ply_path = "./parsing_sphere/sphere_voxel.ply"

# 마칭 큐브 적용 및 회전 후 파일 저장
voxel_array = load_vox_file(vox_file_path)
verts, faces = apply_marching_cubes(voxel_array)

# 면을 반전하여 법선 방향 수정
faces = invert_faces(faces)

# 원하는 방향으로 회전 (예: Z축을 기준으로 90도 회전)
rotated_verts = rotate_vertices(verts, 90, axis='z')

# PLY 파일로 저장
save_as_ply(rotated_verts, faces, output_ply_path)

print(f"PLY 파일로 저장됨: {output_ply_path}")