# --- CELULA: importar helpers e dependencias ---
# Cole esta célula logo após a preparação básica dos dados (feature engineering, encoding, etc.)
from imbalance_helpers import mostrar_balanceamento, montar_pipeline, avaliar_cv, avaliar_final_e_threshold, plot_pr_roc
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Instalar dependências se necessário:
# !pip install -U scikit-learn imbalanced-learn matplotlib seaborn

# Exemplo de uso com seu DataFrame `df` e rótulo `target`:
# X = df.drop(columns=['target'])
# y = df['target'].values

# 1) Mostrar balanceamento
# mostrar_balanceamento(y)

# 2) Separar train/test estratificado
# X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# 3) Montar pipeline com SMOTE dentro (aplica apenas nos folds de treino)
sm = SMOTE(random_state=42)
model = LogisticRegression(solver='liblinear', class_weight='balanced')  # ou RandomForestClassifier(class_weight='balanced')
pipe = montar_pipeline(modelo=model, scaler=True, resampler=sm)

# 4) Avaliar via CV estratificado com métricas robustas (PR-AUC/AP e ROC-AUC)
cvres = avaliar_cv(X_train, y_train, pipe, cv=5, scoring={'ap':'average_precision','roc':'roc_auc'}, n_jobs=-1)
print('CV AP mean:', cvres['test_ap'].mean())
print('CV ROC mean:', cvres['test_roc'].mean())

# 5) Treinar no treino completo e avaliar no test set, ajustando threshold para F1
metrics, y_scores, y_pred = avaliar_final_e_threshold(model, X_train, y_train, X_test, y_test, resampler=sm, threshold_metric='f1')
print(metrics['classification_report'])
print('Best threshold:', metrics['best_threshold'])
plot_pr_roc(y_test, y_scores, label='Modelo final')
