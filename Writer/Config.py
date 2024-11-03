INITIAL_OUTLINE_WRITER_MODEL = "google://gemini-1.5-flash-002"
#gemini-1.5-flash-002

CHAPTER_OUTLINE_WRITER_MODEL = "google://gemini-1.5-flash-002"
CHAPTER_STAGE1_WRITER_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
CHAPTER_STAGE2_WRITER_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
CHAPTER_STAGE3_WRITER_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
CHAPTER_STAGE4_WRITER_MODEL = "google://gemini-1.5-flash-002"
CHAPTER_REVISION_WRITER_MODEL = (
    "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
)
REVISION_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
EVAL_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
INFO_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
SCRUB_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
CHECKER_MODEL = "google://gemini-1.5-flash-002"  # Model used to check results
TRANSLATOR_MODEL = "google://gemini-1.5-flash-002"

MODELS = [
    INITIAL_OUTLINE_WRITER_MODEL,
    CHAPTER_OUTLINE_WRITER_MODEL,
    CHAPTER_STAGE1_WRITER_MODEL,
    CHAPTER_STAGE2_WRITER_MODEL,
    CHAPTER_STAGE3_WRITER_MODEL,
    CHAPTER_STAGE4_WRITER_MODEL,
    CHAPTER_REVISION_WRITER_MODEL,
    REVISION_MODEL,
    EVAL_MODEL,
    INFO_MODEL,
    SCRUB_MODEL,
    CHECKER_MODEL,
    TRANSLATOR_MODEL,
]

BASE_DIR = "story_workdir"

SAVE_PLOT = True
SAVE_CHARACTER_DEVELOPMENT = True
SAVE_DIALOGUE = True

#OLLAMA_CTX = 8192
OLLAMA_CTX = 28192

OLLAMA_HOST = "127.0.0.1:11434"

SEED = 12  # Note this value is overridden by the argparser

TRANSLATE_LANGUAGE = ""  # If the user wants to translate, this'll be changed from empty to a language e.g 'French' or 'Russian'
TRANSLATE_PROMPT_LANGUAGE = ""  # If the user wants to translate their prompt, this'll be changed from empty to a language e.g 'French' or 'Russian'

OUTLINE_QUALITY = 82  # Note this value is overridden by the argparser
OUTLINE_MIN_REVISIONS = 0  # Note this value is overridden by the argparser
OUTLINE_MAX_REVISIONS = 3  # Note this value is overridden by the argparser
CHAPTER_NO_REVISIONS = True  # Note this value is overridden by the argparser # disables all revision checks for the chapter, overriding any other chapter quality/revision settings
CHAPTER_QUALITY = 81  # Note this value is overridden by the argparser
CHAPTER_MIN_REVISIONS = 1  # Note this value is overridden by the argparser
CHAPTER_MAX_REVISIONS = 3  # Note this value is overridden by the argparser

SCRUB_NO_SCRUB = False  # Note this value is overridden by the argparser
EXPAND_OUTLINE = False  # Note this value is overridden by the argparser
ENABLE_FINAL_EDIT_PASS = False  # Note this value is overridden by the argparser

SCENE_GENERATION_PIPELINE = True

OPTIONAL_OUTPUT_NAME = "mastery_unbound241102"

DEBUG = False

# Tested models:
"gemma2:9b"  # works as editor model, DO NOT use as writer model, it sucks
"vanilj/midnight-miqu-70b-v1.5"  # works rather well as the writer, not well as anything else
"command-r"
"qwen:72b"
"command-r-plus"
"nous-hermes2"  # not big enough to really do a good job - do not use
"dbrx"  # sucks - do not use
