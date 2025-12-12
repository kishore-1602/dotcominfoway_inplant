#!/usr/bin/env bash
set -e


PLAYLIST_URL="$1"
OUTPUT_DIR=${2:-data}


if [ -z "$PLAYLIST_URL" ]; then
echo "Usage: $0 <playlist_url> [output_dir]"
exit 1
fi


python ingest_telusko.py --playlist_url "$PLAYLIST_URL" --output_dir "$OUTPUT_DIR"