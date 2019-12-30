#!/usr/bin/env bash


for entry in dataset/*.csv
do
  echo "$entry"
  stat -c %y "$entry"
done
