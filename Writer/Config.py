INITIAL_OUTLINE_WRITER_MODEL = (
    "google://gemini-1.5-pro-001"  # Note this value is overridden by the argparser
)
#gemini-1.5-pro-002

CHAPTER_OUTLINE_WRITER_MODEL = (
    "google://gemini-1.5-pro-002"  # Note this value is overridden by the argparser
)
CHAPTER_STAGE1_WRITER_MODEL = "google://gemini-1.5-pro-001"  # Note this value is overridden by the argparser
CHAPTER_STAGE2_WRITER_MODEL = "google://gemini-1.5-pro-002"  # Note this value is overridden by the argparser
CHAPTER_STAGE3_WRITER_MODEL = "google://gemini-1.5-pro-002"  # Note this value is overridden by the argparser
CHAPTER_STAGE4_WRITER_MODEL = "google://gemini-1.5-pro-002"  # Note this value is overridden by the argparser
CHAPTER_REVISION_WRITER_MODEL = (
    "google://gemini-1.0-pro-001"  # Note this value is overridden by the argparser
)
#REVISION_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser
#ollama://llama3.1

REVISION_MODEL = "google://gemini-1.5-flash-002"  # Note this value is overridden by the argparser

EVAL_MODEL = "ollama://llama3.1"  # Note this value is overridden by the argparser

INFO_MODEL = "ollama://llama3.1"  # Note this value is overridden by the argparser
SCRUB_MODEL = "google://gemini-1.5-pro-002"  # Note this value is overridden by the argparser
CHECKER_MODEL = "ollama://llama3.1"  # Model used to check results
TRANSLATOR_MODEL = "google://gemini-1.5-pro-002"

OLLAMA_CTX = 8192
#OLLAMA_CTX = 28192

OLLAMA_HOST = "127.0.0.1:11434"

SEED = 11  # Note this value is overridden by the argparser

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

OPTIONAL_OUTPUT_NAME = "mlc03"

DEBUG = False

# Tested models:
"gemma2:9b"  # works as editor model, DO NOT use as writer model, it sucks
"llama3.1"  # works as 
"vanilj/midnight-miqu-70b-v1.5"  # works rather well as the writer, not well as anything else
"command-r"
"qwen:72b"
"command-r-plus"
"nous-hermes2"  # not big enough to really do a good job - do not use
"dbrx"  # sucks - do not use
