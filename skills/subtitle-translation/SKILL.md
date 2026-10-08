---
name: subtitle-translation
description: Translate movie or TV subtitle files into Brazilian Portuguese, especially embedded English full and forced tracks extracted from MKV files. Use this skill whenever the user asks to translate subtitles, create a pt-BR subtitle track, process an SRT, or prepare translated subtitles for Jellyfin, Bazarr, or butterbot. It covers extraction, forced-track reconstruction, chunked translation, validation, timestamp-preserving merge, and optional installation beside the media file.
---

# Subtitle Translation

Translate user-provided subtitle material to `pt-BR` without changing its timing. Use the bundled scripts for all mechanical work. Do not ask a translation subagent to rewrite timestamps: chunks contain cue markers and text only, while the original SRT remains the timing source.

## Workflow

1. Create a private work directory outside the repository, such as `$TMPDIR/opencode/subtitles/<slug>`. Never put generated subtitles, media paths, or extracted text in git.
2. Inspect the available tracks. For the common MKV layout, extract the full English track and the forced Japanese-dialogue track with `ffmpeg`:

   ```bash
   ffmpeg -i "MOVIE.mkv" -map 0:FULL_TRACK -f srt work/en.srt \
     -map 0:FORCED_TRACK -f srt work/forced.srt
   ```

   Do not assume track numbers for a new file. Use `ffprobe -v error -select_streams s -show_entries stream=index:stream_tags=language,title -of json` first. Confirm with the user if track identity is ambiguous.
3. If both full and forced tracks exist, run:

   ```bash
   python3 scripts/build_source.py work/en.srt work/forced.srt work/source.srt
   ```

   This removes full-track cues that only say the scene is in Japanese, strips that tag from real text, and interleaves forced cues by timestamp. If there is only one complete subtitle track, copy it as `source.srt` and skip this step.
4. Split the source into balanced translation chunks:

   ```bash
   python3 scripts/split.py work/source.srt work/chunk --chunks 4
   ```

   The output names are `chunk1.en.txt`, `chunk2.en.txt`, and so on. The script prints each cue range.
5. Translate every chunk to Brazilian Portuguese. Parallel translation is fine, but each worker must receive the style guide in `references/pt-br-style-guide.md`. Every cue marker must appear exactly once, in the same range, with at least one non-empty translated line. Write `chunkN.pt.txt` beside its input.
6. Validate each chunk, then combine them in numeric order:

   ```bash
   python3 scripts/check_chunks.py work --chunks 4
   python3 scripts/combine_chunks.py work/chunk work/combined.pt.txt --chunks 4
   ```

7. Merge translated text onto the original timing source:

   ```bash
   python3 scripts/merge_srt.py work/source.srt work/combined.pt.txt work/Movie.pt-BR.srt
   ```

   The merge must report the expected cue count. If it fails, stop and repair the translation rather than guessing or dropping cues.
8. Inspect a sample from the beginning, middle, and end. Check that dialogue dashes, square-bracket sound descriptions, italics, musical notes, names, and honorifics survived appropriately.
9. Only copy the completed file beside the media after validation. For butterbot, use `scp` to the exact movie directory and preserve the filename pattern `Movie.pt-BR.srt`. Do not overwrite an existing file without telling the user first.
10. A Jellyfin refresh is optional. Never print or search for API credentials. If a refresh returns `401`, report that and leave the subtitle installed. Do not retry with guessed keys.

## Translation delegation

For large files, use one general translation worker per chunk. Give each worker:

- The exact input and output paths.
- The cue range and the requirement to preserve every `### N` marker exactly once.
- The pt-BR style guide.
- The relevant `check_chunks.py` command.
- A clear instruction not to refuse user-provided subtitle transformation.

Do not merge a chunk until its validator passes. Do not treat a worker's prose claim as validation: run the checker yourself after all workers finish.

## Safety and reporting

- Never modify the original movie or source subtitles.
- Never commit subtitle output or extracted copyrighted text to a repository.
- Never expose media-server API keys, SSH credentials, or `.env` contents.
- Report source cue count, each chunk validation result, merged cue count, output path, and any failed rescan separately.

Bundled scripts are intentionally small and dependency-free. Read their `--help` output when adapting this workflow to a different subtitle layout.
