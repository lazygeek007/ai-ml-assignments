# AI & ML Assignments

This repository collects my journey through foundational and advanced topics in artificial intelligence and machine learning. Each assignment documents the problem statement, implementation, evaluation, and reflection on what I learned.

---

## Repository Structure

```
ai-ml-assignments/
├── README.md
├── assignments/
│   ├── 01-connect-four/
│   │   ├── README.md
│   │   ├── ConnectFourGame _Final.ipynb
│   │   ├── streamlit_app.py
│   │   └── requirements.txt
│   └── ...
├── data/               # optional: small sample datasets or download scripts
├── notebooks/          # exploratory or shared notebooks
└── utils/              # helper scripts (metrics, plotting, preprocessing)
```

Not every folder will exist from day one—it grows as I progress.

---

## Assignment Index

| # | Topic | Highlights | Status |
| --- | --- | --- | --- |
| 01 | Connect Four Minimax | Depth-limited adversarial search, notebook + Streamlit demo | In Progress |
| 02 | (TBD) |  | Planned |
| 03 | (TBD) |  | Planned |

---

## How I Work

- **Reproducible setups**: environment files (`requirements.txt` / `environment.yml`) per assignment or shared if compatible.  
- **Data handling**: large datasets stay out of git; instead I provide links or download scripts.  
- **Evaluation**: confusion matrices, learning curves, and error analysis accompany each notebook.  
- **Reflection**: every assignment README ends with what worked, what didn’t, and what I’d try next.

---

## Roadmap

- ✅ Scaffold repository and assignment index  
- ⏳ Implement linear regression from scratch and compare with scikit-learn  
- ⏳ Build logistic regression classifier with feature engineering  
- ⏳ Explore neural networks and training dynamics  
- ⏳ Extend into specialized domains (vision, NLP, reinforcement learning)

---

## Tooling

- Python, NumPy, pandas, scikit-learn  
- PyTorch & TensorFlow/Keras for deep learning modules  
- Jupyter/VS Code for notebook-driven experiments  
- MLflow/Weights & Biases (planned) for experiment tracking

---

## Notes

- Start each assignment by duplicating the template README, updating goals, dataset links, and evaluation criteria.  
- Use `pre-commit` hooks or linting (black/flake8) if the assignment grows beyond notebooks.  
- Keep reflections honest—they help future projects and show how thinking evolves.

---

Learning never really ends; this repo keeps me accountable and showcases the progression from fundamentals to applied AI systems.

