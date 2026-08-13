import json
import time


EPSILON = 1e-9


def normalize_label(label):
    """입력 라벨을 표준 라벨(Cross/X)로 변환한다."""
    label = str(label).strip().lower()

    if label in ["+", "cross"]:
        return "Cross"
    elif label in ["x"]:
        return "X"
    else:
        return "UNDECIDED"


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

    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"

def load_data():
    """data.json 파일을 읽어서 반환한다."""
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def main():
    print("=== MAC 필터 판정 프로그램 ===")

    filter_a = read_matrix(3, "필터 A")
    filter_b = read_matrix(3, "필터 B")
    pattern = read_matrix(3, "패턴")

    print("\n--- MAC 계산 ---")

    start = time.perf_counter()

    score_a = mac_score(pattern, filter_a)
    score_b = mac_score(pattern, filter_b)

    end = time.perf_counter()

    result = judge_score(score_a, score_b)

    if result == "A":
        final_result = "Cross"
    elif result == "B":
        final_result = "X"
    else:
        final_result = "UNDECIDED"

    print(f"필터 A 점수 : {score_a:.2f}")
    print(f"필터 B 점수 : {score_b:.2f}")
    print(f"판정 결과   : {final_result}")
    print(f"연산 시간   : {(end - start) * 1000:.6f} ms")

    data = load_data()

    print("\n=== JSON 데이터 확인 ===")
    print(data)

    filters = data["filters"]

    print("\n=== 필터 데이터 확인 ===")
    print(filters)

    print("\n=== Cross 필터 ===")
    print(cross_filter)

    print("\n=== X 필터 ===")
    print(x_filter)

    patterns = data["patterns"]

    print("\n=== 패턴 데이터 확인 ===")
    print(patterns)

    for case_name, case in patterns.items():

        print("\n==============================")
        print(f"CASE : {case_name}")
        print("==============================")

        pattern = case["input"]
        expected = case["expected"]

        size = int(case_name.split("_")[1])
        filter_key = f"size_{size}"
        size_filters = filters[filter_key]

        cross_filter = size_filters["cross"]
        x_filter = size_filters["x"]

        score_cross = mac_score(pattern, cross_filter)
        score_x = mac_score(pattern, x_filter)

        result = judge_score(score_cross, score_x)

        if result == "A":
            final_result = "Cross"
        elif result == "B":
            final_result = "X"
        else:
            final_result = "UNDECIDED"

        print("\n=== JSON MAC 계산 결과 ===")
        print(f"Cross 점수 : {score_cross}")
        print(f"X 점수     : {score_x}")
        print(f"판정 결과  : {final_result}")
        expected_label = normalize_label(expected)

        if final_result == expected_label:
            result_status = "PASS"
        else:
            result_status = "FAIL"

        print(f"Expected   : {expected_label}")
        print(f"Result     : {result_status}")


if __name__ == "__main__":
    main()