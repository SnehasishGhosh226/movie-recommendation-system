# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built with Python, scikit-learn, Pandas, and Streamlit. The system recommends movies based on similarity in their textual metadata and genres rather than relying on user ratings or collaborative filtering.

This project covers the complete workflow from **data preprocessing and exploratory data analysis to feature engineering, model experimentation, similarity-based recommendation, and a Streamlit application**.

---

## ✨ Features

- Content-based movie recommendation
- TF-IDF representation of movie metadata
- Explicit genre similarity using one-hot encoded genres
- Cosine similarity for ranking movies
- Final **80% text similarity + 20% genre similarity** model
- Case-insensitive and whitespace-tolerant movie-title search
- Configurable number of recommendations (5–20)
- Similarity scores displayed with recommendations
- Streamlit web interface
- Precomputed model artifacts for faster application startup

---

## 🧠 How It Works

```text
TMDB Movie Data
      ↓
Data Cleaning & Preprocessing
      ↓
Metadata / Text Feature Engineering
      ↓
TF-IDF ────────────────┐
                       │
Genre Encoding ────────┤
                       ↓
              Similarity Calculation
                       ↓
          80% Text + 20% Genre
                       ↓
              Cosine Similarity
                       ↓
             Ranked Recommendations
```

### 1. Data preprocessing

The TMDB movie metadata contains JSON-like columns such as genres, keywords, production companies, production countries, and spoken languages. These fields were parsed and converted into usable Python structures.

Missing textual values were handled, release dates were converted to datetime values, and movies without meaningful budget/revenue information or without a released status were filtered from the recommendation dataset.

After preprocessing and filtering, the working recommendation dataset contains **3,228 movies**.

### 2. Text representation with TF-IDF

Movie text metadata is combined into a metadata "soup" using information such as:

- Overview
- Tagline
- Genres
- Keywords

The text is cleaned and stemmed before being transformed using **TF-IDF (Term Frequency–Inverse Document Frequency)**.

TF-IDF gives higher importance to terms that are informative for a movie while reducing the influence of very common terms.

### 3. Genre representation

The most frequent genres were one-hot encoded into a numerical genre matrix. This provides an explicit representation of genre similarity rather than relying entirely on words appearing in the movie metadata.

### 4. Cosine similarity

Cosine similarity is used to measure how similar two movie feature representations are.

For the final model, textual similarity and genre similarity are calculated separately and combined as:

```text
Final Similarity
= 0.80 × Text Similarity
+ 0.20 × Genre Similarity
```

The resulting score is used to rank candidate movies.

---

## 🔬 Model Experiments

Several feature configurations were tested during development:

| Model | Features | Observation |
|---|---|---|
| Model 1 | TF-IDF | Strong textual/franchise matching, but sometimes overly literal |
| Model 2 | TF-IDF + Genres | Better genre consistency and broader recommendations |
| Model 3 | TF-IDF + Genres + Numerical Features | Tested budget, revenue, runtime, popularity, ratings and related numerical features |
| Model 4 | Expanded TF-IDF | Added production/company/country/language metadata, but tended to reinforce production/franchise relationships |
| **Final** | **80% Text + 20% Genre** | **Selected as a balanced content-based approach** |

The final weighting was selected through comparative testing of recommendations across different types of movies. This is a qualitative model-selection exercise rather than a claim of measured predictive accuracy, since the dataset does not contain a ground-truth list of movies that each user would consider relevant.

---

## 🎯 Example Recommendations

For **Avatar**, the final model produces:

| Rank | Movie | Similarity Score |
|---:|---|---:|
| 1 | Star Trek Into Darkness | 0.2656 |
| 2 | Independence Day | 0.2653 |
| 3 | Ender's Game | 0.2585 |
| 4 | The Fifth Element | 0.2567 |
| 5 | Titan A.E. | 0.2558 |

For **The Dark Knight**, the model retains strong Batman/franchise relationships while also moving toward broader crime/action/thriller movies.

> **Note:** A similarity score is not a probability that a user will like a movie. It is a relative measure of similarity between feature representations; higher scores indicate greater similarity according to this model.

---

## 🛠️ Tech Stack

- **Python**
- **Pandas** — data manipulation and preprocessing
- **NumPy** — numerical operations
- **scikit-learn** — TF-IDF, feature processing, and cosine similarity
- **NLTK** — Porter stemming for text preprocessing
- **Matplotlib** — exploratory visualization
- **Seaborn** — statistical visualization
- **Streamlit** — interactive web application
- **Joblib** — saving and loading model artifacts
- **Git / GitHub / Git LFS** — version control and large model storage

---

## 📂 Project Structure

```text
movie-recommendation-system/
│
├── app.py                         # Streamlit application
├── movie_recomendation.ipynb      # Data analysis and model development notebook
│
├── final_similarity.pkl           # Final 80:20 similarity matrix
├── movies.pkl                     # Processed movie dataset
├── title_indices.pkl              # Normalized movie-title lookup
│
├── tmdb_5000_movies.csv           # TMDB movie metadata
├── tmdb_5000_credits.csv          # TMDB credits metadata
│
├── .gitignore
├── .gitattributes                 # Git LFS configuration
└── README.md
```

The large `final_similarity.pkl` file is stored using **Git LFS**.

---

## 🚀 Running the Application Locally

### 1. Clone the repository

```bash
git clone https://github.com/SnehasishGhosh226/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install pandas numpy scikit-learn nltk matplotlib seaborn streamlit joblib
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open locally in your browser.

---

## 💻 Using the Application

1. Enter a movie title, for example `Avatar`.
2. Choose the number of recommendations using the slider.
3. Click **Recommend Movies**.
4. The system returns the most similar movies and their similarity scores.

Movie-title lookup is normalized, so differences in capitalization and surrounding whitespace are handled automatically.

---

## 📊 Exploratory Data Analysis

The project includes exploratory analysis of:

- Budget and revenue distributions
- Runtime and popularity distributions
- Vote averages and vote counts
- Correlations between numerical features
- Most frequent movie genres
- Number of movies released over time
- Movie metadata characteristics

The complete analysis and experimentation are available in `movie_recomendation.ipynb`.

---

## ⚠️ Limitations

This is a **content-based** recommender, so recommendations depend entirely on the metadata available in the dataset.

Current limitations include:

- No user-specific preferences or interaction history
- No collaborative filtering
- Similarity does not represent actual user preference
- Recommendations can inherit biases or gaps in the source metadata
- Some movies may receive imperfect recommendations because metadata alone cannot fully capture tone, quality, audience preference, or cultural context
- The current evaluation is primarily qualitative because there is no user-item relevance ground truth in the dataset

A future version could combine content-based recommendations with collaborative filtering or user feedback to create a hybrid recommender.

---

## 🔮 Possible Future Improvements

- Add collaborative filtering using user-rating data
- Build a hybrid recommendation model
- Add movie posters and richer metadata to the interface
- Add fuzzy title matching and autocomplete
- Evaluate recommendations using a suitable offline ranking metric with a ground-truth dataset
- Replace the full similarity matrix with a more memory-efficient nearest-neighbor approach
- Deploy the Streamlit application publicly

---

## 📚 Dataset

The project uses the **TMDB 5000 Movie Dataset**, including movie metadata and credits information.

The dataset is used for educational and machine-learning experimentation purposes.

---

## 👤 Author

**Snehasish Ghosh**

GitHub: [@SnehasishGhosh226](https://github.com/SnehasishGhosh226)

---

## 📄 License

No separate open-source license has been added to this repository yet.
