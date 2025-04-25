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
        return {"type": "leaf", "value": labels[0]}

    col, val = best_split(data)
    if col is None:
        return {"type": "leaf", "value": Counter(labels).most_common(1)[0][0]}

    question = {
        "index": col,
        "feature": feature_names[col],
        "value": val,
        "numeric": is_numeric(val)
    }

    left, right = split_data(data, col, val)

    return {
        "type": "node",
        "question": question,
        "true_branch": build_tree(left, feature_names),
        "false_branch": build_tree(right, feature_names),
    }


def classify(tree, sample, path=None):
    if path is None:
        path = []

    if tree["type"] == "leaf":
        path.append({
            "name": tree["value"],
            "value": tree["value"],
        })

        return {
            "result": tree["value"],
            "path": path
        }

    q = tree["question"]
    val = sample[q["index"]]

    try:
        val = float(val) if q["numeric"] else val
    except:
        return {
            "result": "Неверные данные",
            "path": []
        }

    passed = val <= float(q["value"]) if q["numeric"] else val == q["value"]
    operator = "<=" if q["numeric"] else "=="

    path.append({
        "name": f"{q['feature']} {operator} {q['value']}",
        "feature": q["feature"],
        "value": val,
        "operator": operator,
        "comparison_to": q["value"],
        "passed": passed
    })

    branch = tree["true_branch"] if passed else tree["false_branch"]

    return classify(branch, sample, path)


def to_json(tree):
    if tree["type"] == "leaf":
        return {"type": "leaf", "value": tree["value"]}

    q = tree["question"]

    return {
        "type": "node",
        "question": f"{q['feature']} {'<=' if q['numeric'] else '=='} {q['value']}",
        "true_branch": to_json(tree["true_branch"]),
        "false_branch": to_json(tree["false_branch"]),
    }
