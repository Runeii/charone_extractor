Chara.one extractor

## To use
1.  Add this folder to Blender addons folder
2.  Go to File -> Import -> CharaOne (.one)
3.  Open a CharaOne file
4.  All models from that CharaOne will be added to Blender

## To use in a pipeline
Check the branch `automated-pipeline-processing`. This is an implementation with a modified main.py, which is designed to be able to run over an entire folder of chara.one files. This is not a supported branch, but feel free to check out, use, and modify `main.py` to match your own pipeline needs.

## NOTE REGARDING MAIN CHARACTER MODELS
Main character models (starting with a `d`) do not store their model data inside the charaone, just animations. To import these, you will need to ensure they are alongside the chara.one file in the same folder.

For example:
* myfolder/chara.one
* myfolder/d001.mch

If a mch file is missing, the script will not fail, but it will print a warning to console and skip it.
