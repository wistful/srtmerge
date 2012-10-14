[![Build Status](https://travis-ci.org/[YOUR_GITHUB_USERNAME]/[YOUR_PROJECT_NAME].png)](https://travis-ci.org/[YOUR_GITHUB_USERNAME]/[YOUR_PROJECT_NAME])

### srtmerge

**srtmerge** is a Python library used to merge two Srt files.

## Usage
```python
    from srtmerge import srtmerge
    srtmerge([filepath1, filepath2, ...], out_filepath, offset=1000)
```

`srtmerge filepath1 filepath2 out_filepath offset=1000`