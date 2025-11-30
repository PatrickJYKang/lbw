# LBW Review Dataset (YouTube Highlight Sources)

This repository contains a structured dataset of LBW (Leg Before Wicket) appeals and DRS reviews extracted from official match highlight videos.  
Each entry follows a strict JSON schema, allowing consistent manual logging and enabling downstream analysis or visualisation.

The dataset **excludes compilation videos** and uses only **full-match or extended highlight uploads** from official broadcasters.

---

## Repository Structure

```
├── data.json              # Main dataset containing all videos and deliveries
├── lbw_schema.json        # JSON Schema defining the data requirements
└── validate.py            # Script for validating data.json
```

---

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

---

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

---

## Contributing

All data entries must pass JSON Schema validation before being merged.  
Please follow the existing formatting and naming conventions:

- Timestamps are always `HH:MM:SS`
- Delivery IDs use the format: `inn{n}_ov{over}_ball{ball}`
- Enumerations for DRS components must use the exact spelling defined in the schema

---

## Licence

This dataset is provided for research, cataloguing, and educational purposes.  
Please respect broadcaster copyrights when linking to YouTube material.
