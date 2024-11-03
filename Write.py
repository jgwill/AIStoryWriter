#!/bin/python3

import argparse
import time
import datetime
import os
import json

import Writer.Config

import Writer.Interface.Wrapper
import Writer.PrintUtils
import Writer.Chapter.ChapterDetector
import Writer.Scrubber
import Writer.Statistics
import Writer.OutlineGenerator
import Writer.Chapter.ChapterGenerator
import Writer.StoryInfo
import Writer.NovelEditor
import Writer.Translator
from Writer.Interface.Wrapper import Interface  # Add missing import


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Prompt", help="Path to file containing the prompt")
Parser.add_argument(
    "-Output",
    "-Output",
    default="",
    type=str,
    help="Optional file output path, if none is speciifed, we will autogenerate a file name based on the story title",
)
Parser.add_argument(
    "-InitialOutlineModel",
    default=Writer.Config.INITIAL_OUTLINE_WRITER_MODEL,
    type=str,
    help="Model to use for writing the base outline content",
)
Parser.add_argument(
    "-ChapterOutlineModel",
    default=Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL,
    type=str,
    help="Model to use for writing the per-chapter outline content",
)
Parser.add_argument(
    "-ChapterS1Model",
    default=Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 1: plot)",
)
Parser.add_argument(
    "-ChapterS2Model",
    default=Writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 2: character development)",
)
Parser.add_argument(
    "-ChapterS3Model",
    default=Writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 3: dialogue)",
)
Parser.add_argument(
    "-ChapterS4Model",
    default=Writer.Config.CHAPTER_STAGE4_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 4: final correction pass)",
)
Parser.add_argument(
    "-ChapterRevisionModel",
    default=Writer.Config.CHAPTER_REVISION_WRITER_MODEL,
    type=str,
    help="Model to use for revising the chapter until it meets criteria",
)
Parser.add_argument(
    "-RevisionModel",
    default=Writer.Config.REVISION_MODEL,
    type=str,
    help="Model to use for generating constructive criticism",
)
Parser.add_argument(
    "-EvalModel",
    default=Writer.Config.EVAL_MODEL,
    type=str,
    help="Model to use for evaluating the rating out of 100",
)
Parser.add_argument(
    "-InfoModel",
    default=Writer.Config.INFO_MODEL,
    type=str,
    help="Model to use when generating summary/info at the end",
)
Parser.add_argument(
    "-ScrubModel",
    default=Writer.Config.SCRUB_MODEL,
    type=str,
    help="Model to use when scrubbing the story at the end",
)
Parser.add_argument(
    "-CheckerModel",
    default=Writer.Config.CHECKER_MODEL,
    type=str,
    help="Model to use when checking if the LLM cheated or not",
)
Parser.add_argument(
    "-TranslatorModel",
    default=Writer.Config.TRANSLATOR_MODEL,
    type=str,
    help="Model to use if translation of the story is enabled",
)
Parser.add_argument(
    "-Translate",
    default="",
    type=str,
    help="Specify a language to translate the story to - will not translate by default. Ex: 'French'",
)
Parser.add_argument(
    "-TranslatePrompt",
    default="",
    type=str,
    help="Specify a language to translate your input prompt to. Ex: 'French'",
)
Parser.add_argument("-Seed", default=12, type=int, help="Used to seed models.")
Parser.add_argument(
    "-OutlineMinRevisions",
    default=0,
    type=int,
    help="Number of minimum revisions that the outline must be given prior to proceeding",
)
Parser.add_argument(
    "-OutlineMaxRevisions",
    default=3,
    type=int,
    help="Max number of revisions that the outline may have",
)
Parser.add_argument(
    "-ChapterMinRevisions",
    default=0,
    type=int,
    help="Number of minimum revisions that the chapter must be given prior to proceeding",
)
Parser.add_argument(
    "-ChapterMaxRevisions",
    default=3,
    type=int,
    help="Max number of revisions that the chapter may have",
)
Parser.add_argument(
    "-NoChapterRevision", action="store_true", help="Disables Chapter Revisions"
)
Parser.add_argument(
    "-NoScrubChapters",
    action="store_true",
    help="Disables a final pass over the story to remove prompt leftovers/outline tidbits",
)
Parser.add_argument(
    "-ExpandOutline",
    action="store_true",
    default=True,
    help="Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content",
)
Parser.add_argument(
    "-EnableFinalEditPass",
    action="store_true",
    help="Enable a final edit pass of the whole story prior to scrubbing",
)
Parser.add_argument(
    "-Debug",
    action="store_true",
    help="Print system prompts to stdout during generation",
)
Parser.add_argument(
    "-SceneGenerationPipeline",
    action="store_true",
    default=True,
    help="Use the new scene-by-scene generation pipeline as an initial starting point for chapter writing",
)
Parser.add_argument(
    "-SleepTime",
    default=20,
    type=int,
    help="Time to wait between requests in seconds",
)
Parser.add_argument(
    "--SavePlot",
    action="store_true",
    help="Save the plot stage to a file",
)
Parser.add_argument(
    "--SaveCharacterDevelopment",
    action="store_true",
    help="Save the character development stage to a file",
)
Parser.add_argument(
    "--SaveDialogue",
    action="store_true",
    help="Save the dialogue stage to a file",
)
Parser.add_argument(
    "--BaseDir",
    type=str,
    default="story_workdir",
    help="Directory to save the stages",
)

Args = Parser.parse_args()


# Measure Generation Time
StartTime = time.time()


# Setup Config
Writer.Config.SEED = Args.Seed

Writer.Config.INITIAL_OUTLINE_WRITER_MODEL = Args.InitialOutlineModel
Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL = Args.ChapterOutlineModel
Writer.Config.CHAPTER_STAGE1_WRITER_MODEL = Args.ChapterS1Model
Writer.Config.CHAPTER_STAGE2_WRITER_MODEL = Args.ChapterS2Model
Writer.Config.CHAPTER_STAGE3_WRITER_MODEL = Args.ChapterS3Model
Writer.Config.CHAPTER_STAGE4_WRITER_MODEL = Args.ChapterS4Model
Writer.Config.CHAPTER_REVISION_WRITER_MODEL = Args.ChapterRevisionModel
Writer.Config.EVAL_MODEL = Args.EvalModel
Writer.Config.REVISION_MODEL = Args.RevisionModel
Writer.Config.INFO_MODEL = Args.InfoModel
Writer.Config.SCRUB_MODEL = Args.ScrubModel
Writer.Config.CHECKER_MODEL = Args.CheckerModel
Writer.Config.TRANSLATOR_MODEL = Args.TranslatorModel

Writer.Config.TRANSLATE_LANGUAGE = Args.Translate
Writer.Config.TRANSLATE_PROMPT_LANGUAGE = Args.TranslatePrompt

Writer.Config.OUTLINE_MIN_REVISIONS = Args.OutlineMinRevisions
Writer.Config.OUTLINE_MAX_REVISIONS = Args.OutlineMaxRevisions

Writer.Config.CHAPTER_MIN_REVISIONS = Args.ChapterMinRevisions
Writer.Config.CHAPTER_MAX_REVISIONS = Args.ChapterMaxRevisions
Writer.Config.CHAPTER_NO_REVISIONS = Args.NoChapterRevision

Writer.Config.SCRUB_NO_SCRUB = Args.NoScrubChapters
Writer.Config.EXPAND_OUTLINE = Args.ExpandOutline
Writer.Config.ENABLE_FINAL_EDIT_PASS = Args.EnableFinalEditPass

Writer.Config.OPTIONAL_OUTPUT_NAME = Args.Output
Writer.Config.SCENE_GENERATION_PIPELINE = Args.SceneGenerationPipeline
Writer.Config.DEBUG = Args.Debug

interface = Interface()
plot, char_dev, dialogue = interface.process_stages()

SLEEP_TIME = Args.SleepTime

base_dir = Args.BaseDir
os.makedirs(base_dir)

if Args.SavePlot:
    plot_path = os.path.join(base_dir, "plot_stage.txt")
    with open(plot_path, "w") as f:
        f.write(plot)

if Args.SaveCharacterDevelopment:
    char_dev_path = os.path.join(base_dir, "character_development_stage.txt")
    with open(char_dev_path, "w") as f:
        f.write(char_dev)

if Args.SaveDialogue:
    dialogue_path = os.path.join(base_dir, "dialogue_stage.txt")
    with open(dialogue_path, "w") as f:
        f.write(dialogue)

# Get a list of all used providers
Models = [
    Writer.Config.INITIAL_OUTLINE_WRITER_MODEL,
    Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE4_WRITER_MODEL,
    Writer.Config.CHAPTER_REVISION_WRITER_MODEL,
    Writer.Config.EVAL_MODEL,
    Writer.Config.REVISION_MODEL,
    Writer.Config.INFO_MODEL,
    Writer.Config.SCRUB_MODEL,
    Writer.Config.CHECKER_MODEL,
    Writer.Config.TRANSLATOR_MODEL,
]
Models = list(set(Models))

# Setup Logger
SysLogger = Writer.PrintUtils.Logger()

# Initialize Interface
SysLogger.Log("Created OLLAMA Interface", 5)
Interface = Writer.Interface.Wrapper.Interface(Models)

# Load User Prompt
Prompt: str = ""
if Args.Prompt is None:
    raise Exception("No Prompt Provided")
with open(Args.Prompt, "r") as f:
    Prompt = f.read()


# If user wants their prompt translated, do so
if Writer.Config.TRANSLATE_PROMPT_LANGUAGE != "":
    Prompt = Writer.Translator.TranslatePrompt(
        Interface, SysLogger, Prompt, Writer.Config.TRANSLATE_PROMPT_LANGUAGE
    )


# Generate the Outline
Outline, Elements, RoughChapterOutline, BaseContext = Writer.OutlineGenerator.GenerateOutline(
    Interface, SysLogger, Prompt, Writer.Config.OUTLINE_QUALITY
)
BasePrompt = Prompt


# Detect the number of chapters
SysLogger.Log("Detecting Chapters", 5)
Messages = [Interface.BuildUserQuery(Outline)]
NumChapters: int = Writer.Chapter.ChapterDetector.LLMCountChapters(
    Interface, SysLogger, Interface.GetLastMessageText(Messages)
)
SysLogger.Log(f"Found {NumChapters} Chapter(s)", 5)


## Write Per-Chapter Outline
Prompt = f"""
Please help me expand upon the following outline, chapter by chapter.

```
{Outline}
```
    
"""
Messages = [Interface.BuildUserQuery(Prompt)]
ChapterOutlines: list = []
if Writer.Config.EXPAND_OUTLINE:
    for Chapter in range(1, NumChapters + 1):
        ChapterOutline, Messages = Writer.OutlineGenerator.GeneratePerChapterOutline(
            Interface, SysLogger, Chapter, Outline, Messages
        )
        ChapterOutlines.append(ChapterOutline)
        time.sleep(SLEEP_TIME)


# Create MegaOutline
DetailedOutline: str = ""
for Chapter in ChapterOutlines:
    DetailedOutline += Chapter
MegaOutline: str = f"""

# Base Outline
{Elements}

# Detailed Outline
{DetailedOutline}

"""

# Setup Base Prompt For Per-Chapter Generation
UsedOutline: str = Outline
if Writer.Config.EXPAND_OUTLINE:
    UsedOutline = MegaOutline


# Write the chapters
SysLogger.Log("Starting Chapter Writing", 5)
Chapters = []
for i in range(1, NumChapters + 1):
    try:
        Chapter = Writer.Chapter.ChapterGenerator.GenerateChapter(
            Interface,
            SysLogger,
            i,
            NumChapters,
            Outline,
            Chapters,
            Writer.Config.OUTLINE_QUALITY,
            BaseContext,
        )
        time.sleep(SLEEP_TIME)

        Chapter = f"### Chapter {i}\n\n{Chapter}"
        Chapters.append(Chapter)
        ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
        SysLogger.Log(f"Chapter Word Count: {ChapterWordCount}", 2)

    except Exception as e:
        SysLogger.Log(f"Failed to generate Chapter {i}: {str(e)}", 1)
        # Implement retry logic or append a placeholder to maintain list consistency
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            SysLogger.Log(f"Retrying Chapter {i} generation (Attempt {retry_count + 1})", 2)
            try:
                Chapter = Writer.Chapter.ChapterGenerator.GenerateChapter(
                    Interface,
                    SysLogger,
                    i,
                    NumChapters,
                    Outline,
                    Chapters,
                    Writer.Config.OUTLINE_QUALITY,
                    BaseContext,
                )
                time.sleep(SLEEP_TIME)

                Chapter = f"### Chapter {i}\n\n{Chapter}"
                Chapters.append(Chapter)
                ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
                SysLogger.Log(f"Chapter Word Count: {ChapterWordCount}", 2)
                break  # Exit retry loop on success
            except Exception as retry_e:
                time.sleep(2)
                if '429' in str(retry_e):
                    SysLogger.Log(f"429 Error: Quota exceeded. Waiting 60 seconds before retrying.", 2)
                    time.sleep(60)
                SysLogger.Log(f"Retry {retry_count + 1} failed for Chapter {i}: {str(retry_e)}", 1)
                retry_count += 1
        else:
            SysLogger.Log(f"Failed to generate Chapter {i} after {max_retries} retries. Skipping.", 1)
            Chapters.append(f"### Chapter {i}\n\n*Generation Failed: Chapter skipped.*")

# Load stages if they exist
if os.path.exists(plot_path):
    with open(plot_path, "r") as f:
        plot = f.read()

if os.path.exists(char_dev_path):
    with open(char_dev_path, "r") as f:
        char_dev = f.read()

if os.path.exists(dialogue_path):
    with open(dialogue_path, "r") as f:
        dialogue = f.read()

# Now edit the whole thing together
StoryBodyText: str = ""
StoryInfoJSON:dict = {"Outline": Outline}
StoryInfoJSON.update({"StoryElements": Elements})
StoryInfoJSON.update({"RoughChapterOutline": RoughChapterOutline})
StoryInfoJSON.update({"BaseContext": BaseContext})

if Writer.Config.ENABLE_FINAL_EDIT_PASS:
    NewChapters = Writer.NovelEditor.EditNovel(
        Interface, SysLogger, Chapters, Outline, NumChapters
    )
NewChapters = Chapters
StoryInfoJSON.update({"UnscrubbedChapters": NewChapters})

# Now scrub it (if enabled)
if not Writer.Config.SCRUB_NO_SCRUB:
    NewChapters = Writer.Scrubber.ScrubNovel(
        Interface, SysLogger, NewChapters, NumChapters
    )
else:
    SysLogger.Log(f"Skipping Scrubbing Due To Config", 4)
StoryInfoJSON.update({"ScrubbedChapter": NewChapters})


# If enabled, translate the novel
if Writer.Config.TRANSLATE_LANGUAGE != "":
    NewChapters = Writer.Translator.TranslateNovel(
        Interface, SysLogger, NewChapters, NumChapters, Writer.Config.TRANSLATE_LANGUAGE
    )
else:
    SysLogger.Log(f"No Novel Translation Requested, Skipping Translation Step", 4)
StoryInfoJSON.update({"TranslatedChapters": NewChapters})


# Compile The Story
for Chapter in NewChapters:
    StoryBodyText += Chapter + "\n\n\n"


# Now Generate Info
Messages = []
Messages.append(Interface.BuildUserQuery(Outline))
Info = Writer.StoryInfo.GetStoryInfo(Interface, SysLogger, Messages)
Title = Info["Title"]
StoryInfoJSON.update({"Title": Info["Title"]})
Summary = Info["Summary"]
StoryInfoJSON.update({"Summary": Info["Summary"]})
Tags = Info["Tags"]
StoryInfoJSON.update({"Tags": Info["Tags"]})

print("---------------------------------------------")
print(f"Story Title: {Title}")
print(f"Summary: {Summary}")
print(f"Tags: {Tags}")
print("---------------------------------------------")

ElapsedTime = time.time() - StartTime


# Calculate Total Words
TotalWords: int = Writer.Statistics.GetWordCount(StoryBodyText)
SysLogger.Log(f"Story Total Word Count: {TotalWords}", 4)

StatsString: str = "Work Statistics:  \n"
StatsString += " - Total Words: " + str(TotalWords) + "  \n"
StatsString += f" - Title: {Title}  \n"
StatsString += f" - Summary: {Summary}  \n"
StatsString += f" - Tags: {Tags}  \n"
StatsString += f" - Generation Start Date: {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}  \n"
StatsString += f" - Generation Total Time: {ElapsedTime}s  \n"
StatsString += f" - Generation Average WPM: {60 * (TotalWords/ElapsedTime)}  \n"

StatsString += "\n\nUser Settings:  \n"
StatsString += f" - Base Prompt: {BasePrompt}  \n"

StatsString += "\n\nGeneration Settings:  \n"
StatsString += f" - Generator: AIStoryGenerator_2024-06-27  \n"
StatsString += (
    f" - Base Outline Writer Model: {Writer.Config.INITIAL_OUTLINE_WRITER_MODEL}  \n"
)
StatsString += (
    f" - Chapter Outline Writer Model: {Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL}  \n"
)
StatsString += f" - Chapter Writer (Stage 1: Plot) Model: {Writer.Config.CHAPTER_STAGE1_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 2: Char Development) Model: {Writer.Config.CHAPTER_STAGE2_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 3: Dialogue) Model: {Writer.Config.CHAPTER_STAGE3_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 4: Final Pass) Model: {Writer.Config.CHAPTER_STAGE4_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Revision) Model: {Writer.Config.CHAPTER_REVISION_WRITER_MODEL}  \n"
StatsString += f" - Revision Model: {Writer.Config.REVISION_MODEL}  \n"
StatsString += f" - Eval Model: {Writer.Config.EVAL_MODEL}  \n"
StatsString += f" - Info Model: {Writer.Config.INFO_MODEL}  \n"
StatsString += f" - Scrub Model: {Writer.Config.SCRUB_MODEL}  \n"
StatsString += f" - Seed: {Writer.Config.SEED}  \n"
# StatsString += f" - Outline Quality: {Writer.Config.OUTLINE_QUALITY}  \n"
StatsString += f" - Outline Min Revisions: {Writer.Config.OUTLINE_MIN_REVISIONS}  \n"
StatsString += f" - Outline Max Revisions: {Writer.Config.OUTLINE_MAX_REVISIONS}  \n"
# StatsString += f" - Chapter Quality: {Writer.Config.CHAPTER_QUALITY}  \n"
StatsString += f" - Chapter Min Revisions: {Writer.Config.CHAPTER_MIN_REVISIONS}  \n"
StatsString += f" - Chapter Max Revisions: {Writer.Config.CHAPTER_MAX_REVISIONS}  \n"
StatsString += f" - Chapter Disable Revisions: {Writer.Config.CHAPTER_NO_REVISIONS}  \n"
StatsString += f" - Disable Scrubbing: {Writer.Config.SCRUB_NO_SCRUB}  \n"


# Save The Story To Disk
SysLogger.Log("Saving Story To Disk", 3)
os.makedirs("Stories", exist_ok=True)
FName = f"Stories/Story_{Title.replace(' ', '_')}"
if Writer.Config.OPTIONAL_OUTPUT_NAME != "":
    FName = Writer.Config.OPTIONAL_OUTPUT_NAME
with open(f"{FName}.md", "w", encoding="utf-8") as F:
    Out = f"""
{StatsString}

---

Note: An outline of the story is available at the bottom of this document.
Please scroll to the bottom if you wish to read that.

---
# {Title}

{StoryBodyText}


---
# Outline
```
{Outline}
```
"""
    SysLogger.SaveStory(Out)
    F.write(Out)

# Save JSON
with open(f"{FName}.json", "w", encoding="utf-8") as F:
    F.write(json.dumps(StoryInfoJSON, indent=4))
    F.write(json.dumps(StoryInfoJSON, indent=4))