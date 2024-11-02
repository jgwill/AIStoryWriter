import Writer.PrintUtils
import Writer.Prompts


def ScrubNovel(Interface, _Logger, EditedChapters, NumChapters):
    ScrubbedChapters = []
    for i in range(1, NumChapters + 1):
        if i - 1 < len(EditedChapters):
            try:
                Prompt: str = Writer.Prompts.CHAPTER_SCRUB_PROMPT.format(
                    _Chapter=EditedChapters[i - 1]
                )
                _Logger.Log(f"Prompting LLM To Perform Chapter {i} Scrubbing Edit", 5)
                Messages = []
                Messages.append(Interface.BuildUserQuery(Prompt))
                Messages = Interface.SafeGenerateText(
                    _Logger, Messages, Writer.Config.SCRUB_MODEL
                )
                _Logger.Log(f"Finished Chapter {i} Scrubbing Edit", 5)

                NewChapter = Interface.GetLastMessageText(Messages)
                scrubbed = NewChapter
                ScrubbedChapters.append(scrubbed)
                ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
                _Logger.Log(f"Scrubbed Chapter Word Count: {ChapterWordCount}", 3)
            except Exception as e:
                _Logger.Log(f"Error scrubbing Chapter {i}: {str(e)}", 1)
                ScrubbedChapters.append(EditedChapters[i - 1])  # Append original if scrub fails
        else:
            _Logger.Log(f"Missing Chapter {i} during scrubbing.", 2)
            ScrubbedChapters.append("")  # Append empty string or handle appropriately
    return ScrubbedChapters
