import time
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test

FEATURES = [
    'sepal length (cm)', 'sepal width (cm)',
    'petal length (cm)', 'petal width (cm)'
]

@transformer
def train(df, *args, **kwargs):
    train_df = df[df['split'] == 'train']
    test_df = df[df['split'] == 'test'].copy()

    results = []
    predictions = {}

    for depth in range(1, 6):
        model = DecisionTreeClassifier(max_depth=depth, random_state=42)

        start = time.perf_counter()
        model.fit(train_df[FEATURES], train_df['target'])
        pred = model.predict(test_df[FEATURES])
        elapsed = time.perf_counter() - start

        accuracy = (pred == test_df['target']).mean()
        results.append({
            'max_depth': depth,
            'accuracy': round(accuracy, 4),
            'runtime_seconds': round(elapsed, 4)
        })
        predictions[depth] = pred

    print(pd.DataFrame(results).to_string(index=False))

    test_df['predicted'] = predictions[3]
    return test_df


@test
def test_output(output, *args):
    assert len(output) == 30
    assert 'predicted' in output.columns