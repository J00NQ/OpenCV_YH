import numpy as np

# 2행 3열 행렬 생성
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print("--- 기본 행렬 ---")
print(matrix)
print(f"모양(Shape): {matrix.shape}") # (2, 3) 출력

# 모든 원소가 0인 3x3 행렬
zeros = np.zeros((3, 3))

# 모든 원소가 1인 2x2 행렬
ones = np.ones((2, 2))

# 단위 행렬 (Identity Matrix)
identity = np.eye(3)

print("--- 단위 행렬 ---")
print(identity)

# 0부터 11까지 12개의 원소를 가진 3x4 행렬 생성
range_matrix = np.arange(12).reshape(3, 4)

print("--- 3x4 재구조화 행렬 ---")
print(range_matrix)

# 0~255 사이의 정수 난수로 채워진 5x5 행렬 (uint8 타입)
gray_image_mock = np.random.randint(0, 256, (5, 5), dtype=np.uint8)

print("--- 가상 그레이스케일 데이터 (5x5) ---")
print(gray_image_mock)