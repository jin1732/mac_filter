import json

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
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
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

    required_sizes = [5, 13, 25]

    for size in required_sizes:
        key = f"size_{size}"

        if key not in filters:
            print(f"필터 오류: {key}가 없습니다.")
            return False

    for pattern_key, pattern_data in patterns.items():

        parts = pattern_key.split("_")

        if len(parts) < 3 or parts[0] != "size":
            print(f"패턴 키 형식 오류: {pattern_key}")
            continue

        try:
            size = int(parts[1])
        except ValueError:
            print(f"패턴 크기 오류: {pattern_key}")
            continue

        filter_key = f"size_{size}"

        if filter_key not in filters:
            print(f"{pattern_key}: 해당 필터 {filter_key}가 없습니다.")
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

        input_data = pattern_data["input"]

        if len(input_data) != size:
            print(f"{pattern_key}: 행 크기 불일치")
            continue

        valid_rows = True

        for row in input_data:
            if len(row) != size:
                valid_rows = False
                break

        if not valid_rows:
            print(f"{pattern_key}: 열 크기 불일치")
            continue
        
    print("JSON 기본 구조 및 크기 검증 완료")
    return True

def analyze_json_data(data):
    filters = data["filters"]
    patterns = data["patterns"]

    for pattern_key, pattern_data in patterns.items():

        parts = pattern_key.split("_")

        if len(parts) < 3 or parts[0] != "size":
            print(f"\n패턴 키 형식 오류: {pattern_key}")
            continue

        try:
            size = int(parts[1])
        except ValueError:
            print(f"\n패턴 크기 오류: {pattern_key}")
            continue

        filter_key = f"size_{size}"

        if filter_key not in filters:
            print(f"\n{pattern_key}: {filter_key} 필터가 없습니다.")
            continue

        pattern = pattern_data["input"]

        cross_filter = filters[filter_key]["cross"]
        x_filter = filters[filter_key]["x"]

        cross_score = mac_score(pattern, cross_filter)
        x_score = mac_score(pattern, x_filter)

        print(f"\n===== {pattern_key} =====")
        print(f"Cross 점수: {cross_score}")
        print(f"X 점수: {x_score}")

filter_a = read_matrix_3x3("필터 A")
filter_b = read_matrix_3x3("필터 B")
pattern = read_matrix_3x3("패턴")

score_a = mac_score(pattern, filter_a)
score_b = mac_score(pattern, filter_b)

result = judge_score(score_a, score_b)

print("\nMAC 결과")
print(f"필터 A 점수: {score_a}")
print(f"필터 B 점수: {score_b}")
print(f"판정 결과: {result}")

data = load_json_data("data.json")

if data is not None:
    print("\ndata.json 로드 성공")
    print("최상위 키:", list(data.keys()))

    validate_json_data(data)