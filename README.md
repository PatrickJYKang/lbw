# LBW Review Dataset (YouTube Highlight Sources)

This repository contains a structured dataset of LBW (Leg Before Wicket) appeals and DRS reviews extracted from official match highlight videos.  
Each entry follows a strict JSON schema, allowing consistent manual logging and enabling downstream analysis or visualisation.

The dataset **excludes compilation videos** and uses only **full-match or extended highlight uploads** from official broadcasters.

## Repository Structure

```
├── data.json              # Main dataset containing all videos and deliveries
├── lbw_schema.json        # JSON Schema defining the data requirements
└── validate.py            # Script for validating data.json
```

## JSON Structure Overview

Each **video** corresponds to one highlight upload.  
Each **delivery** corresponds to a single LBW appeal, including:

- metadata (bowler, batter, over, ball, teams)
- on-field decision and final decision
- full DRS components:
  - pitching (in-line / outside-off / outside-leg / umpire’s call)
  - impact (in-line / outside-off / umpire’s call)
  - wickets (hitting / missing / umpire’s call)
- two clips:
  - `delivery` (run-up → on-field decision)
  - `review` (ball-tracking → third umpire decision)

Unavailable numerical fields are recorded as -1.

The full schema is defined in `lbw_schema.json`.

## Validation

### Requirements
Install the validator dependency:

```
pip install jsonschema
```

### Run validation

```
python validate.py data.json
```

If the JSON passes validation:

```
Valid!
```

If errors are found, the script will print a precise error message showing where the structure deviates from the schema.

## A Note on Data Quality

This dataset is **not** intended for use in statistical applications, such as training machine learning models, because it is **not** a representative sample of all LBW appeals and reviews; that is, it is a completely discretionary selection of videos and deliveries. There may even be multiple LBW appeals in the same video/match, of which only one or two has been logged. Of course, feel free to add more data to the dataset, although do still keep in mind the purpose of the dataset when doing so. 

The factual accuracy of the data is maintained to the best of my ability but it is not guaranteed. Please do report or fix any errors you may find. Data not contained within the video is usually obtained from the match report from ESPNcricinfo. 

Much of the logging work is done by a LLM, which is unfortunately prone to hallucination. Commonly, the LLM may misidentify the first name of the bowler, batter, or umpire, or may misidentify the over or ball. Although the LLM does no research, it may pretend to. If you intend to contribute to the dataset using a LLM, please double-check **the data it enters into the dataset** for accuracy.

---

## Contributing

All data entries must pass JSON Schema validation before being merged.  
Please follow the existing formatting and naming conventions:

- Timestamps are always `HH:MM:SS`
- Delivery IDs use the format: `inn{n}_ov{over}_ball{ball}`; if any of those are unknown, use lowercase letters
- Enumerations for DRS components must use the exact spelling defined in the schema

---

## Licence

This dataset is released into the public domain under the CC0 1.0 Universal dedication. It contains only factual metadata and manually logged timestamps.

The public domain licence applies only to the dataset itself.
**All referenced YouTube videos remain the property of their respective rights holders. No video content is hosted, stored, or redistributed in this repository.**

Users are responsible for ensuring that any use of the linked video material complies with YouTube’s Terms of Service and applicable copyright law.
