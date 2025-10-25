# Helpers para tratar desbalanceamento e avaliar modelos (para usar no classificacao.ipynb)
# Requer: scikit-learn, imbalanced-learn, matplotlib, seaborn
# pip install -U scikit-learn imbalanced-learn matplotlib seaborn

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split, RandomizedSearchCV
from sklearn.metrics import (confusion_matrix, classification_report,
                             precision_recall_curve, average_precision_score,
                             roc_auc_score, precision_score, recall_score,
                             f1_score, roc_curve)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline as SkPipeline

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, TomekLinks
from imblearn.combine import SMOTEENN, SMOTETomek

def mostrar_balanceamento(y, ax=None):
    """
    Plota a distribuição de classes.
    y: array-like de rótulos
    """
    cnt = Counter(y)
    labels = list(map(str, cnt.keys()))
    values = list(cnt.values())
    if ax is None:
        fig, ax = plt.subplots(1,1, figsize=(5,3))
    sns.barplot(x=labels, y=values, palette='Blues', ax=ax)
    ax.set_title('Distribuição de classes')
    ax.set_xlabel('Classe')
    ax.set_ylabel('Contagem')
    for i, v in enumerate(values):
        ax.text(i, v + max(values)*0.01, str(v), ha='center')

def montar_pipeline(modelo, scaler=True, resampler=None):
    """
    Retorna uma pipeline do imblearn com (opcional) scaler e resampler.
    - modelo: estimador scikit-learn
    - scaler: True -> StandardScaler
    - resampler: None ou objeto do imblearn (ex: SMOTE(), RandomUnderSampler())
    IMPORTANTE: coloque o resampler ANTES do estimador (aplica só no treino em CV)
    """
    steps = []
    if scaler:
        steps.append(('scaler', StandardScaler()))
    if resampler is not None:
        steps.append(('resampler', resampler))
    steps.append(('estimator', modelo))
    return ImbPipeline(steps)

def avaliar_cv(X, y, pipeline, cv=5, scoring=None, n_jobs=1):
    """
    Faz cross-validate estratificado. Retorna dict com scores.
    - pipeline: pipeline do imblearn (resampler dentro se quiser)
    - scoring: lista ou dict de métricas (ex: ['roc_auc','average_precision'])
    """
    if scoring is None:
        scoring = {'roc_auc': 'roc_auc', 'average_precision': 'average_precision'}
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    cvres = cross_validate(pipeline, X, y, cv=skf, scoring=scoring, return_train_score=False, n_jobs=n_jobs)
    return cvres

def grid_search_pipeline(pipeline, param_dist, X, y, cv=5, n_iter=50, n_jobs=1, scoring='average_precision'):
    """
    RandomizedSearchCV sobre uma pipeline do imblearn.
    - param_dist: dicionário de distribuição de parâmetros (preﬁxados com <step>__param se for pipeline)
    - scoring: métrica principal (ex: 'average_precision' para PR-AUC)
    Retorna o objeto RandomizedSearchCV ajustado.
    """
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    rs = RandomizedSearchCV(pipeline, param_distributions=param_dist, n_iter=n_iter,
                            scoring=scoring, cv=skf, n_jobs=n_jobs, random_state=42, verbose=1)
    rs.fit(X, y)
    return rs

def ajustar_threshold(y_true, y_scores, metric='f1'):
    """
    Busca threshold que maximiza a métrica escolhida (f1, recall, precision).
    - y_scores: probabilidades da classe positiva (array)
    Retorna (melhor_threshold, dict_threshold_to_score)
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_scores)
    best_t = 0.5
    best_score = -np.inf
    scores_map = {}
    # thresholds array tem len = len(precisions)-1
    for i, t in enumerate(np.append(thresholds, 1.0)):
        p = precisions[i]
        r = recalls[i]
        if metric == 'f1':
            if p + r == 0:
                s = 0
            else:
                s = 2 * p * r / (p + r)
        elif metric == 'precision':
            s = p
        elif metric == 'recall':
            s = r
        else:
            raise ValueError('metric must be f1/precision/recall')
        scores_map[float(t)] = s
        if s > best_score:
            best_score = s
            best_t = float(t)
    return best_t, scores_map

def plot_pr_roc(y_true, y_scores, ax=None, label=None):
    """
    Plota curvas Precision-Recall (com average precision) e ROC (com AUC).
    """
    if ax is None:
        fig, axs = plt.subplots(1,2, figsize=(12,4))
    else:
        axs = ax
    # PR
    precisions, recalls, _ = precision_recall_curve(y_true, y_scores)
    ap = average_precision_score(y_true, y_scores)
    axs[0].plot(recalls, precisions, label=f'{label or ""} AP={ap:.3f}')
    axs[0].set_xlabel('Recall')
    axs[0].set_ylabel('Precision')
    axs[0].set_title('Precision-Recall')
    axs[0].legend()
    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    auroc = roc_auc_score(y_true, y_scores)
    axs[1].plot(fpr, tpr, label=f'{label or ""} AUROC={auroc:.3f}')
    axs[1].plot([0,1],[0,1],'--', color='gray')
    axs[1].set_xlabel('FPR')
    axs[1].set_ylabel('TPR')
    axs[1].set_title('ROC')
    axs[1].legend()

def avaliar_final_e_threshold(model, X_train, y_train, X_test, y_test, resampler=None, scaler=True, threshold_metric='f1'):
    """
    Ajusta modelo com resampling (se fornecido) e retorna relatório no test set, mais threshold recomendado.
    - model: estimador sklearn
    - resampler: objeto imblearn (ex: SMOTE())
    """
    pipe = montar_pipeline(modelo=model, scaler=scaler, resampler=resampler)
    pipe.fit(X_train, y_train)
    # probabilidades da classe positiva
    if hasattr(pipe, 'predict_proba'):
        y_scores = pipe.predict_proba(X_test)[:,1]
    else:
        # estimadores sem predict_proba -> decision_function (ex: SVM) ou predict
        if hasattr(pipe, 'decision_function'):
            y_scores = pipe.decision_function(X_test)
            # normalize to 0-1
            y_scores = (y_scores - y_scores.min()) / (y_scores.max() - y_scores.min() + 1e-12)
        else:
            y_scores = pipe.predict(X_test).astype(float)
    best_t, scores_map = ajustar_threshold(y_test, y_scores, metric=threshold_metric)
    y_pred_thresh = (y_scores >= best_t).astype(int)
    cm = confusion_matrix(y_test, y_pred_thresh)
    report = classification_report(y_test, y_pred_thresh, digits=4)
    metrics = {
        'confusion_matrix': cm,
        'classification_report': report,
        'best_threshold': best_t,
        'average_precision': average_precision_score(y_test, y_scores),
        'roc_auc': roc_auc_score(y_test, y_scores),
    }
    return metrics, y_scores, y_pred_thresh

# Fim do arquivo
