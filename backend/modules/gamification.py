import pandas as pd

def gamify(df):
    """
    Assign points, levels, badges, and progress toward top performer.
    """
    # 1. Points calculation
    df['points'] = (
        df['deliveries_completed'] * 2 +
        df['sales_made'] * 3 +
        df['customer_rating'] * 15 +
        df['attendance_days'] * 1
    )

    # 2. Dynamic Levels based on percentiles
    q25 = df['points'].quantile(0.25)
    q50 = df['points'].quantile(0.50)
    q75 = df['points'].quantile(0.75)

    def level(p):
        if p <= q25:
            return 'Bronze'
        elif p <= q50:
            return 'Silver'
        elif p <= q75:
            return 'Gold'
        else:
            return 'Platinum'

    df['level'] = df['points'].apply(level)

    # 3. Badges based on performance
    top_10_percent = df['points'].quantile(0.9)
    top_25_percent = df['points'].quantile(0.75)

    def badge(p):
        if p >= top_10_percent:
            return '🌟 Star Performer'
        elif p >= top_25_percent:
            return '🏅 High Achiever'
        elif p >= q50:
            return '🎯 Goal Getter'
        else:
            return '👍 Participant'

    df['badge'] = df['points'].apply(badge)

    # 4. Progress toward top performer
    max_points = df['points'].max()
    df['progress'] = df['points'] / max_points

    return df