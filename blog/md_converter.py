def md_convert(md_text):
    """
    Convert markdown text to html text
    """
    import markdown
    return markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])