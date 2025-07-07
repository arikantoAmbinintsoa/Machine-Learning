def train_model():
    """Entraîne un GradientBoostingClassifier sur le dataset CSV et sauvegarde le modèle."""
    import pandas as pd
    from pathlib import Path
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    import seaborn as sns
    import matplotlib.pyplot as plt
    import joblib

    CSV_PATH = Path('data/Tic_tac_initial_results.csv')

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"{CSV_PATH} introuvable. Placez le fichier dans le dossier data/.")

    print(f"Lecture {CSV_PATH} …")
    df = pd.read_csv(CSV_PATH)

    move_cols = [c for c in df.columns if c.lower().startswith('move')]
    df[move_cols] = df[move_cols].replace({'?': -1}).astype(int)
    label_map = {'loss': 0, 'draw': 1, 'win': 2}
    df['CLASS'] = df['CLASS'].map(label_map)

    X = df[move_cols].values
    y = df['CLASS'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print("Train:", X_train.shape, "Test:", X_test.shape)

    model = GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=['loss','draw','win']))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['loss','draw','win'], yticklabels=['loss','draw','win'])
    plt.xlabel('Prédictions')
    plt.ylabel('Vérités')
    plt.title('Matrice de confusion')
    plt.show()

    Path("models").mkdir(parents=True, exist_ok=True)
    joblib.dump(model, "models/gbm.pkl")
    print("Modèle sauvegardé dans models/gbm.pkl")