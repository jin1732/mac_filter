import json
import time


def mac_score(pattern, filter_data):
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score

def measure_performance(filter_a, pattern):
    sizes = [3, 5, 13, 25]
    repeat = 10

    print("\n===== 성능 분석 =====")
    print("크기(N×N)   | 평균 시간(ms) | 연산 횟수(N²)")
    print("--------------------------------------------")

    for size in sizes:

        if size == 3:
            test_pattern = pattern
            test_filter = filter_a

        else:
            test_pattern = [
                [1.0 for _ in range(size)]
                for _ in range(size)
            ]

            test_filter = [
                [1.0 for _ in range(size)]
                for _ in range(size)
            ]

        total_time = 0.0

        for _ in range(repeat):

            start = time.perf_counter()

            mac_score(
                test_pattern,
                test_filter
            )

            end = time.perf_counter()

            total_time += (end - start) * 1000

        average_time = total_time / repeat

        operation_count = size * size

        print(
            f"{size:>2}×{size:<2} | "
            f"{average_time:>12.6f} | "
            f"{operation_count:>8}"
        )

def measure_performance_3x3(filter_a, pattern):
    repeat = 10

    print("\n===== 성능 분석 =====")
    print("크기(N×N)   | 평균 시간(ms) | 연산 횟수(N²)")
    print("--------------------------------------------")

    total_time = 0.0

    for _ in range(repeat):

        start = time.perf_counter()

        mac_score(
            pattern,
            filter_a
        )

        end = time.perf_counter()

        total_time += (end - start) * 1000

    average_time = total_time / repeat
    operation_count = 3 * 3

    print(
        f"{3:>2}×{3:<2} | "
        f"{average_time:>12.6f} | "
        f"{operation_count:>8}"
    )

def mac_score(pattern, filter_data):
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score


def judge_score(score_a, score_b):
    epsilon = 1e-9

    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"

    elif score_a > score_b:
        return "A"

    else:
        return "B"


def normalize_label(label):
    label = str(label).strip().lower()

    if label == "+" or label == "cross":
        return "Cross"

    elif label == "x":
        return "X"

    else:
        return None


def read_matrix_3x3(name):
    print(f"\n{name} 입력")

    matrix = []

    for i in range(3):

        while True:

            row = input(f"{i + 1}행: ").split()

            if len(row) != 3:
                print(
                    "입력 형식 오류: "
                    "각 줄에 3개의 숫자를 공백으로 구분해 입력하세요."
                )
                continue

            try:
                row = [float(value) for value in row]
                matrix.append(row)
                break

            except ValueError:
                print("입력 형식 오류: 숫자만 입력하세요.")

    return matrix


def load_json_data(filename):
    try:

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except FileNotFoundError:

        print(f"파일을 찾을 수 없습니다: {filename}")
        return None

    except json.JSONDecodeError:

        print(f"JSON 형식 오류: {filename}")
        return None


# =========================================================
# JSON 기본 구조 및 크기 검증
# =========================================================

def validate_json_data(data):

    if not isinstance(data, dict):
        print("JSON 형식 오류: 최상위 데이터가 딕셔너리가 아닙니다.")
        return False

    if "filters" not in data:
        print("JSON 구조 오류: filters가 없습니다.")
        return False

    if "patterns" not in data:
        print("JSON 구조 오류: patterns가 없습니다.")
        return False

    filters = data["filters"]
    patterns = data["patterns"]

    if not isinstance(filters, dict):
        print("JSON 구조 오류: filters가 딕셔너리가 아닙니다.")
        return False

    if not isinstance(patterns, dict):
        print("JSON 구조 오류: patterns가 딕셔너리가 아닙니다.")
        return False

    # -----------------------------------------------------
    # size_5, size_13, size_25 필터 존재 여부 확인
    # -----------------------------------------------------

    required_sizes = [5, 13, 25]

    for size in required_sizes:

        key = f"size_{size}"

        if key not in filters:
            print(f"필터 오류: {key}가 없습니다.")
            return False

    # -----------------------------------------------------
    # patterns의 키와 기본 구조 확인
    # -----------------------------------------------------

    for pattern_key, pattern_data in patterns.items():

        parts = pattern_key.split("_")

        # size_N_idx 형식 확인
        if len(parts) < 3 or parts[0] != "size":

            print(f"패턴 키 형식 오류: {pattern_key}")
            continue

        try:
            size = int(parts[1])

        except ValueError:

            print(f"패턴 크기 오류: {pattern_key}")
            continue

        # 해당 size_N 필터가 존재하는지 확인
        filter_key = f"size_{size}"

        if filter_key not in filters:

            print(
                f"{pattern_key}: "
                f"해당 필터 {filter_key}가 없습니다."
            )
            continue

        if not isinstance(pattern_data, dict):

            print(f"{pattern_key}: 데이터 형식 오류")
            continue

        if "input" not in pattern_data:

            print(f"{pattern_key}: input이 없습니다.")
            continue

        if "expected" not in pattern_data:

            print(f"{pattern_key}: expected가 없습니다.")
            continue

        # -------------------------------------------------
        # 패턴 N x N 크기 확인
        # -------------------------------------------------

        input_data = pattern_data["input"]

        if not isinstance(input_data, list):

            print(
                f"{pattern_key}: "
                "input 데이터가 리스트가 아닙니다."
            )
            continue

        if len(input_data) != size:

            print(
                f"{pattern_key}: "
                f"행 크기 불일치 "
                f"(actual: {len(input_data)}, expected: {size})"
            )
            continue

        row_error = False

        for row in input_data:

            if not isinstance(row, list):

                row_error = True
                break

            if len(row) != size:

                row_error = True
                break

        if row_error:

            print(
                f"{pattern_key}: "
                f"열 크기 불일치 "
                f"(expected: {size})"
            )
            continue

    print("JSON 기본 구조 및 크기 검증 완료")

    return True


# =========================================================
# JSON 데이터 분석
# =========================================================

def analyze_json_data(data):

    filters = data["filters"]
    patterns = data["patterns"]

    total = 0
    passed = 0
    failed = 0

    failed_cases = []

    for pattern_key, pattern_data in patterns.items():

        total += 1

        # -------------------------------------------------
        # 1. 패턴 키 확인
        # -------------------------------------------------

        parts = pattern_key.split("_")

        if len(parts) < 3 or parts[0] != "size":

            reason = "패턴 키 형식 오류"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        # -------------------------------------------------
        # 2. N 추출
        # -------------------------------------------------

        try:

            size = int(parts[1])

        except ValueError:

            reason = "패턴 크기 오류"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        # -------------------------------------------------
        # 3. size_N 필터 선택
        # -------------------------------------------------

        filter_key = f"size_{size}"

        if filter_key not in filters:

            reason = f"{filter_key} 필터가 없음"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        # -------------------------------------------------
        # 4. pattern_data 구조 확인
        # -------------------------------------------------

        if not isinstance(pattern_data, dict):

            reason = "패턴 데이터 형식 오류"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        if "input" not in pattern_data:

            reason = "input 없음"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        if "expected" not in pattern_data:

            reason = "expected 없음"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        pattern = pattern_data["input"]

        # -------------------------------------------------
        # 5. 패턴 N x N 크기 검증
        # -------------------------------------------------

        if not isinstance(pattern, list):

            reason = "패턴 데이터가 리스트가 아님"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        if len(pattern) != size:

            reason = (
                f"패턴 행 크기 불일치 "
                f"(actual: {len(pattern)}, expected: {size})"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        row_error = False

        for row in pattern:

            if not isinstance(row, list):

                row_error = True
                break

            if len(row) != size:

                row_error = True
                break

        if row_error:

            reason = (
                f"패턴 열 크기 불일치 "
                f"(expected: {size})"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        # -------------------------------------------------
        # 6. 필터 확인
        # -------------------------------------------------

        filter_data = filters[filter_key]

        if not isinstance(filter_data, dict):

            reason = f"{filter_key} 필터 데이터 형식 오류"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        if "cross" not in filter_data or "x" not in filter_data:

            reason = (
                f"{filter_key}에 Cross/X 필터가 없음"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        cross_filter = filter_data["cross"]
        x_filter = filter_data["x"]

        # -------------------------------------------------
        # 7. Cross 필터 N x N 크기 검증
        # -------------------------------------------------

        if not isinstance(cross_filter, list):

            reason = "Cross 필터 데이터가 리스트가 아님"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        if len(cross_filter) != size:

            reason = (
                f"Cross 필터 행 크기 불일치 "
                f"(actual: {len(cross_filter)}, expected: {size})"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        cross_error = False

        for row in cross_filter:

            if not isinstance(row, list):

                cross_error = True
                break

            if len(row) != size:

                cross_error = True
                break

        if cross_error:

            reason = (
                f"Cross 필터 열 크기 불일치 "
                f"(expected: {size})"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        # -------------------------------------------------
        # 8. X 필터 N x N 크기 검증
        # -------------------------------------------------

        if not isinstance(x_filter, list):

            reason = "X 필터 데이터가 리스트가 아님"

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        if len(x_filter) != size:

            reason = (
                f"X 필터 행 크기 불일치 "
                f"(actual: {len(x_filter)}, expected: {size})"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        x_error = False

        for row in x_filter:

            if not isinstance(row, list):

                x_error = True
                break

            if len(row) != size:

                x_error = True
                break

        if x_error:

            reason = (
                f"X 필터 열 크기 불일치 "
                f"(expected: {size})"
            )

            print(f"\n{pattern_key}: FAIL - {reason}")

            failed += 1
            failed_cases.append((pattern_key, reason))

            continue

        # -------------------------------------------------
        # 9. MAC 계산
        # -------------------------------------------------

        cross_score = mac_score(
            pattern,
            cross_filter
        )

        x_score = mac_score(
            pattern,
            x_filter
        )

        # -------------------------------------------------
        # 10. 판정
        # -------------------------------------------------

        result = judge_score(
            cross_score,
            x_score
        )

        if result == "A":

            result_label = "Cross"

        elif result == "B":

            result_label = "X"

        else:

            result_label = "UNDECIDED"

        # -------------------------------------------------
        # 11. expected 정규화
        # -------------------------------------------------

        expected_label = normalize_label(
            pattern_data["expected"]
        )

        # -------------------------------------------------
        # 12. 결과 출력
        # -------------------------------------------------

        print(f"\n===== {pattern_key} =====")

        print(f"Cross 점수: {cross_score}")
        print(f"X 점수: {x_score}")
        print(f"판정: {result_label}")
        print(f"expected: {expected_label}")

        # -------------------------------------------------
        # 13. PASS / FAIL 비교
        # -------------------------------------------------

        if result_label == expected_label:

            print("결과: PASS")

            passed += 1

        else:

            reason = (
                f"판정 불일치 "
                f"(판정: {result_label}, "
                f"expected: {expected_label})"
            )

            print(f"결과: FAIL - {reason}")

            failed += 1

            failed_cases.append(
                (pattern_key, reason)
            )

    # =====================================================
    # 결과 요약
    # =====================================================

    print("\n===== 결과 요약 =====")

    print(f"전체 테스트: {total}")
    print(f"통과: {passed}")
    print(f"실패: {failed}")

    if failed_cases:

        print("\n===== 실패 케이스 =====")

        for case, reason in failed_cases:

            print(f"- {case}: FAIL - {reason}")

# =========================================================
# Mode 1 - 3x3 사용자 입력
# =========================================================

def run_mode1():

    filter_a = read_matrix_3x3("필터 A")
    print("필터 A 저장 완료")

    filter_b = read_matrix_3x3("필터 B")
    print("패턴 저장 완료")

    pattern = read_matrix_3x3("패턴")
    print("패턴 저장 완료")

    # MAC 계산
    score_a = mac_score(
        pattern,
        filter_a
    )

    score_b = mac_score(
        pattern,
        filter_b
    )

    # 판정
    result = judge_score(
        score_a,
        score_b
    )

    print("\n===== MAC 결과 =====")

    print(f"필터 A 점수: {score_a}")
    print(f"필터 B 점수: {score_b}")
    print(f"판정 결과: {result}")

    # 3×3 성능 분석만 실행
    measure_performance_3x3(
        filter_a,
        pattern
    )


# =========================================================
# Mode 2 - data.json 분석
# =========================================================

def run_mode2():

    data = load_json_data("data.json")

    if data is None:
        return

    print("\ndata.json 로드 성공")

    print(
        "최상위 키:",
        list(data.keys())
    )

    if validate_json_data(data):

        analyze_json_data(data)

        # 3×3 성능 측정을 위한 테스트 데이터
        test_pattern = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]

        test_filter = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]

        # 성능 분석
        measure_performance(
            test_filter,
            test_pattern
        )


# =========================================================
# 메인 메뉴
# =========================================================

def main():

    while True:

        print("\n===================================")
        print("       Mini NPU MAC Filter")
        print("===================================")

        print("1. 사용자 입력 (3×3)")
        print("2. data.json 분석")
        print("3. 프로그램 종료")

        choice = input("\n모드를 선택하세요: ")

        if choice == "1":

            run_mode1()

        elif choice == "2":

            run_mode2()

        elif choice == "3":

            print("\n프로그램을 종료합니다.")
            break

        else:

            print("\n입력이 올바르지 않습니다.")
            print("1, 2, 3 중에서 선택하세요.")


# =========================================================
# 프로그램 실행
# =========================================================

if __name__ == "__main__":
    main()