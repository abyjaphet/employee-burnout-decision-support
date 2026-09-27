from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import shap

ROOT = Path(__file__).resolve().parents[1]
_explainer = None


def _get_explainer():
    global _explainer
    if _explainer is None:
        _explainer = joblib.load(ROOT / "models" / "shap_explainer.pkl")
    return _explainer


def get_shap_explanation(employee_df, predicted_class=None):
    """
    Returns:
        shap_values : SHAP Explanation object
        top_driver : str
        top5 : pandas.DataFrame with Feature, SHAP, ABS
    """
    shap_values = _get_explainer()(employee_df)
    values = shap_values.values

    if values.ndim == 3:
        class_idx = 0 if predicted_class is None else int(predicted_class)
        signed = values[0, :, class_idx]
    elif values.ndim == 2:
        signed = values[0]
    else:
        signed = values

    importance = pd.DataFrame(
        {
            "Feature": list(employee_df.columns),
            "SHAP": list(signed),
        }
    )
    importance["ABS"] = importance["SHAP"].abs()
    importance = importance.sort_values(by="ABS", ascending=False)

    top_driver = importance.iloc[0]["Feature"]
    top5 = importance.head(5).copy()
    return shap_values, top_driver, top5


def plot_waterfall(shap_values, predicted_class):
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(8, 5), facecolor="#152033")

    shap.plots.waterfall(
        shap_values[0, :, predicted_class],
        show=False,
    )
    fig = plt.gcf()
    fig.patch.set_facecolor("#152033")
    for ax in fig.axes:
        ax.set_facecolor("#152033")
        ax.tick_params(colors="#E8EEF7")
        ax.xaxis.label.set_color("#E8EEF7")
        ax.yaxis.label.set_color("#E8EEF7")
        for spine in ax.spines.values():
            spine.set_color("#334155")
    return fig
