# Manual Test Log - TheFoodINC v0.2

## Current status

The Streamlit prototype is working.

Confirmed features:
- Image upload works
- Keras model loads successfully
- Top-5 predictions are displayed
- Confidence threshold works
- Product info cards are displayed for confident predictions
- Product info cards are hidden or softened for uncertain predictions
- Low reliability class warning works

## Good results

- Pear: high confidence and correct prediction
- Cucumber: high confidence and correct prediction

## Acceptable uncertain results

- Chilli pepper: correct top-1 prediction but below threshold
- Green plum-like images: confused with tomato/apple/papaya and marked as uncertain

## Known model issues

- Plum may not appear in Top-5 for some green plum images
- Leafy greens such as mint, parsley, and chard may be confused
- Stylized stock photos or distant market images may reduce confidence

## Next steps

- Improve UI layout
- Add confidence bar
- Add user guidance for unclear images
- Later investigate plum dataset/model behavior