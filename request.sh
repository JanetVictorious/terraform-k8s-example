#!/bin/bash

while sleep 0.01;

do curl -X POST http://127.0.0.1:52873/predict \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "island": "Torgersen",
  "culmen_length_mm": 39.1,
  "culmen_depth_mm": 18.7,
  "flipper_length_mm": 181,
  "body_mass_g": 3750,
  "sex": "MALE"
}';

done
