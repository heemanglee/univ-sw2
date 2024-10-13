import numpy as np
from pyvox.parser import VoxParser
from skimage import measure
import trimesh

def load_voxel_data(filename):
    # .vox 파일 로드
    vox = VoxParser(filename).parse()
    
    # 복셀 데이터 추출
    model = vox.models[0]
    size = model.size  # (x, y, z)
    x_size, y_size, z_size = size
    voxel_data = np.zeros((z_size, y_size, x_size), dtype=np.uint8)  # z, y, x 순서
    
    for voxel in model.voxels:
        x, y, z = voxel.x, voxel.y, voxel.z
        voxel_data[z, y, x] = 1  # 복셀 값 설정
    
    return voxel_data

def generate_mesh(voxel_data):
    verts, faces, normals, values = measure.marching_cubes(voxel_data, level=0.5)
    # 면의 버텍스 순서 반전
    faces = faces[:, ::-1]
    return verts, faces

def smooth_mesh(verts, faces):
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    # 메쉬 스무딩 적용 (Taubin Smoothing)
    mesh = trimesh.smoothing.filter_taubin(mesh, lamb=0.5, nu=-0.53, iterations=10)
    return mesh.vertices, mesh.faces

def save_mesh_to_file(verts, faces, filename):
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    # 메쉬 정리 및 법선 벡터 재계산
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces()
    mesh.invert()  # 면의 방향 반전
    mesh.fix_normals()  # 법선 벡터 재계산
    # 메쉬 저장
    mesh.export(filename)

def main():
    # 1. 복셀 데이터 로드
    voxel_data = load_voxel_data('bunny_small.vox')  # 파일명 변경 필요
    print('복셀 데이터 로드 완료')
    
    # 2. 메쉬 생성
    verts, faces = generate_mesh(voxel_data)
    print('메쉬 생성 완료')
    
    # 3. 토러스 패치 적용 (여기서는 메쉬 스무딩으로 대체)
    verts, faces = smooth_mesh(verts, faces)
    print('메쉬 스무딩 완료')
    
    # 4. 결과 메쉬 저장
    save_mesh_to_file(verts, faces, 'smoothed_voxel.obj')
    print('메쉬가 "smoothed_voxel.obj" 파일로 저장되었습니다.')

if __name__ == '__main__':
    main()