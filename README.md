# Nepal Crop Yield Prediction

An end-to-end ML project predicting crop yields in Nepal from rainfall patterns.

## Key Findings
- Random Forest R² = **0.776** (5-fold shuffled CV)
- Rainfall + crop type explain ~78% of yield variance
- Detected & removed feature leakage from the `year` column (had inflated R² to 0.99)

## Tech Stack
Python · pandas · SQLite · scikit-learn · Streamlit

## Project Structure