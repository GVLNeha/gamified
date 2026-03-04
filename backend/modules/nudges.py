def generate_nudge(points):
    """
    Generate a personalized nudge based on points.
    """
    if points < 50:
        return "Try focusing on your key tasks this month!"
    elif points < 100:
        return "Good job! Keep improving your performance!"
    elif points < 150:
        return "Great work! You are doing very well!"
    else:
        return "Excellent performance! Keep up the amazing work!"

def add_nudges(df):
    """
    Add a 'nudge' column to the DataFrame based on points.
    """
    df['nudge'] = df['points'].apply(generate_nudge)
    return df