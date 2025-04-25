import math
from collections import Counter


def entropy(data):
    label_counts = Counter(row[-1] for row in data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in label_counts.values())


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def split_data(data, col, value):
    if is_numeric(value):
        left = [row for row in data if float(row[col]) <= float(value)]
        right = [row for row in data if float(row[col]) > float(value)]
    else:
        left = [row for row in data if row[col] == value]
        right = [row for row in data if row[col] != value]

    return left, right


def best_split(data):
    best_gain = 0
    best_col = None
    best_value = None
    base_entropy = entropy(data)
    n_features = len(data[0]) - 1

    for col in range(n_features):
        values = set(row[col] for row in data)
        for val in values:
            left, right = split_data(data, col, val)
            if not left or not right:
                continue
            p = len(left) / len(data)
            gain = base_entropy - (p * entropy(left) + (1 - p) * entropy(right))
            if gain > best_gain:
                best_gain, best_col, best_value = gain, col, val

    return best_col, best_value


def build_tree(data, feature_names):
    labels = [row[-1] for row in data]
    if labels.count(labels[0]) == len(labels):
        return labels[0]

    if len(feature_names) == 0 or len(data[0]) == 1:
        return Counter(labels).most_common(1)[0][0]

    col, val = best_split(data)
    if col is None:
        return Counter(labels).most_common(1)[0][0]

    left, right = split_data(data, col, val)

    question = {
        "feature": feature_names[col],
        "value": val,
        "numeric": is_numeric(val),
    }

    remaining_features = feature_names[:col] + feature_names[col + 1:]

    left_data = [[row[i] for i in range(len(row)) if i != col] for row in left]
    right_data = [[row[i] for i in range(len(row)) if i != col] for row in right]

    return {
        "question": question,
        "true_branch": build_tree(left_data, remaining_features),
        "false_branch": build_tree(right_data, remaining_features),
    }


def classify(tree, feature_names, sample, path=None):
    if path is None:
        path = []

    if not isinstance(tree, dict):
        return {
            "result": tree,
            "path": path
        }

    q = tree["question"]
    feature_index = feature_names.index(q["feature"])
    val = sample[feature_index]

    try:
        val = float(val) if q["numeric"] else val
    except:
        path.append({
            "feature": q["feature"],
            "value": val,
            "operator": "<=" if q["numeric"] else "==",
            "passed": "Ошибка приведения типов"
        })
        return {
            "result": "Неверные данные",
            "path": path
        }

    compare = val <= float(q["value"]) if q["numeric"] else val == q["value"]
    operator = "<=" if q["numeric"] else "=="

    path.append({
        "feature": q["feature"],
        "value": val,
        "operator": operator,
        "comparison_to": q["value"],
        "passed": compare
    })

    branch = tree["true_branch"] if compare else tree["false_branch"]

    new_sample = sample[:feature_index] + sample[feature_index + 1:]
    new_features = feature_names[:feature_index] + feature_names[feature_index + 1:]

    return classify(branch, new_features, new_sample, path)


def to_json(tree):
    if not isinstance(tree, dict):
        return {"type": "leaf", "value": tree}

    q = tree["question"]

    return {
        "type": "node",
        "question": f"{q['feature']} {'<=' if q['numeric'] else '=='} {q['value']}",
        "true_branch": to_json(tree["true_branch"]),
        "false_branch": to_json(tree["false_branch"]),
    }
