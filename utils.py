def loading_bar(percentage):
    loading_txt = f"              Loading... 0%"
    loading_bar = "|                                               |"

    if percentage == 0:
        return f"```\n{loading_txt}\n{loading_bar}\n```"

    segments = 100
    seg_length = len(loading_bar) / segments

    loading_txt = f"              Loading... {percentage}%"
    loading_bar = f"|{'='*int(seg_length*percentage)}{' '*int(seg_length*(segments-percentage))}|"

    return f"```\n{loading_txt}\n{loading_bar}\n```"
