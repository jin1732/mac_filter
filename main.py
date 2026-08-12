import json
import time


EPSILON = 1e-9


def normalize_label(label):
    """입력 라벨을 표준 라벨로 변환한다."""
    pass


def mac_score(pattern, filter_data):
    n = len(pattern)
    total = 0.0

    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filter_data[i][j]

    return total

def read_matrix(size, name):
    """size x size 크기의 행렬을 입력받는다."""
    while True:
        print(f"\n[{name} 입력]")
        matrix = []

        try:
            for i in range(size):
                while True:
                    row = input(
                        f"{i + 1}행 ({size}개의 숫자): "
                    ).split()

                    if len(row) != size:
                        print(
                            f"입력 형식 오류: "
                            f"각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요."
                        )
                        continue

                    try:
                        row = [float(value) for value in row]
                        matrix.append(row)
                        break

                    except ValueError:
                        print("입력 형식 오류: 숫자만 입력하세요.")

            return matrix

        except KeyboardInterrupt:
            print("\n입력을 취소했습니다.")
            return None
        
def judge_score(score_a, score_b):
    """두 점수를 비교하여 판정한다."""
    pass


def main():
    print("=== MAC 필터 판정 프로그램 ===")
    
    filter_a = read_matrix(3, "필터 A")

    print("\n입력된 필터 A:")
    for row in filter_a:
        print(row)


if __name__ == "__main__":
    main()